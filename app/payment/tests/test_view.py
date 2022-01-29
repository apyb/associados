from unittest import mock
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils import timezone
from model_bakery import baker
from django.core import mail

from app.members.models import Member, Category
from app.payment import views
from app.payment.models import Payment, Transaction, PaymentType, AVAILABLE
from app.payment.views import PaymentView, NotificationView


class MemberTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username="Wolverine",
            email='logan@xmen.org',
            first_name='James',
            last_name='Howlett',
        )
        self.member = baker.make(
            Member,
            user=self.user,
            category=Category.objects.get(id=1)
        )


class PaymentViewTestCase(MemberTestCase):

    def setUp(self):
        super(PaymentViewTestCase, self).setUp()

        self.url = reverse('payments:payment', kwargs=dict(member_id=42))
        self.request = RequestFactory().get("/", {})
        self.request.user = self.user

        self.requests_original = views.requests

        class ResponseMock(object):
            content = "<code>xpto123</code>"

            def ok(self):
                return True

        def post(self, *args, **kwargs):
            return ResponseMock()

        views.requests.post = post

    def tearDown(self):
        views.requests = self.requests_original
        Payment.objects.all().delete()

    def test_response_302(self):
        resp = self._get_payment_endpoint()
        self.assertEqual(302, resp.status_code)

    def test_redirection_has_correct_url(self):
        resp = self._get_payment_endpoint()
        self.assertEqual(
            'https://pagseguro.uol.com.br/v2/checkout/'
            'payment.html?code=xpto123',
            resp.url
        )

    @mock.patch('app.payment.views.get_object_or_404')
    def _get_payment_endpoint(self, mock_get_404):
        mock_get_404.return_value = self.member
        return self.client.get(self.url)

    def test_payment_view_should_redirect_to_dashboard_if_it_fails_to_create_the_transaction(self):
        class ResponseMock(object):
            content = None

            @property
            def ok(self):
                return False

        requests_original = views.requests
        try:
            views.requests.post = lambda self, *args, **kwargs: ResponseMock()
            request = RequestFactory().get("/", {})
            v = PaymentView()
            v._notify_staff = lambda u: None
            response = v.dispatch(request, self.member.id)
            self.assertFalse(Payment.objects.filter(member=self.member).exists())
            self.assertEqual(302, response.status_code)
            self.assertEqual("/", response["Location"])
        finally:
            views.requests = requests_original

    def test_payment_view_should_create_a_payment_for_the_current_user_and_redirect_to_payment_gateway(self):
        response = PaymentView.as_view()(self.request, self.member.id)
        self.assertTrue(Payment.objects.filter(member=self.member).exists())
        self.assertEqual(302, response.status_code)
        expected_url = settings.PAYMENT_ENDPOINT_WEBCHECKOUT + "xpto123"
        self.assertEqual(expected_url, response["Location"])

    def test_payment_view_should_create_a_payment_for_the_user_type(self):
        self.assertEqual(Payment.objects.filter(member=self.member).count(), 0)
        PaymentView.as_view()(self.request, self.member.id)
        self.assertEqual(Payment.objects.filter(member=self.member).count(), 1)

    def test_generate_transaction(self):
        payment = Payment.objects.create(
            member=self.member,
            type=PaymentType.objects.get(id=1)
        )
        transaction = PaymentView().set_payment_code(payment)
        self.assertEqual("xpto123", transaction.code)


class NotificationViewTestCase(MemberTestCase):

    @classmethod
    def setUpClass(cls):
        #call_command("loaddata", "profiles.json", verbosity=0)
        pass

    @classmethod
    def tearDownClass(cls):
        #call_command("flush", interactive=False, verbosity=0)
        pass

    def setUp(self):
        super(NotificationViewTestCase, self).setUp()

        self.user = User.objects.get(username="Wolverine")
        self.requests_original = views.requests

        class ResponseMock(object):
            content = "<xml><status>3</status><reference>3</reference><grossAmount>1.00</grossAmount></xml>"

            def ok(self):
                return True

        def get(self, *args, **kwargs):
            return ResponseMock()

        views.requests.get = get

    def tearDown(self):
        views.requests = self.requests_original

    def _make_transaction(self, status, code, price):
        payment = Payment.objects.create(
            member=self.member,
            type=PaymentType.objects.get(id=2)
        )
        transaction = Transaction.objects.create(
            payment=payment,
            status=status,
            code=code,
            price=price
        )
        return payment, transaction

    def test_name_url(self):
        try:
            reverse('payments:notification')
        except NoReverseMatch:
            self.fail("Reversal of url named 'notification' failed with NoReverseMatch")

    def test_transaction_should_get_info_about_transaction(self):
        status, ref, price = NotificationView().transaction("code")
        self.assertEqual("3", status)
        self.assertEqual(3, ref)
        self.assertEqual(1.00, price)

    def test_transaction_done_update_member_category(self):
        payment, transaction = self._make_transaction(status=1, code="xpto", price="123.54")
        view = NotificationView()
        view.transaction_code = 'xpto'
        view.transaction_done(payment.id)

        reloaded_member = Member.objects.get(id=self.member.id)
        self.assertEqual(reloaded_member.category, payment.type.category)

    def test_transaction_done_fill_payment_date(self):
        payment, transaction = self._make_transaction(status=1, code="xpto", price="123.54")
        self.assertFalse(payment.date)
        view = NotificationView()
        view.transaction_code = 'xpto'
        view.transaction_done(payment.id)

        reloaded_payment = Payment.objects.get(id=payment.id)
        self.assertTrue(reloaded_payment.date)
        self.assertEqual(
            reloaded_payment.date.strftime('%Y-%m-%d+%H:%M'),
            timezone.now().strftime('%Y-%m-%d+%H:%M')
        )

    def test_transaction_done_fill_payment_valid_until(self):
        payment, transaction = self._make_transaction(status=1, code="xpto", price="123.54")
        self.assertFalse(payment.valid_until)
        view = NotificationView()
        view.transaction_code = 'xpto'
        view.transaction_done(payment.id)

        valid_until = timezone.now() + timedelta(days=payment.type.duration)
        reloaded_payment = Payment.objects.get(id=payment.id)
        self.assertTrue(reloaded_payment.valid_until)
        self.assertEqual(reloaded_payment.valid_until.strftime('%Y-%m-%d+%H:%M'),
                         valid_until.strftime('%Y-%m-%d+%H:%M'))

    def test_transaction_done_should_respect_last_payment_date(self):
        payment, transaction = self._make_transaction(status=1, code="xpto", price="123.54")
        valid_until = timezone.now() + timedelta(days=payment.type.duration)
        view = NotificationView()
        view.transaction_code = 'xpto'
        view.transaction_done(payment.id)

        reloaded_payment = Payment.objects.get(id=payment.id)
        self.assertEqual(reloaded_payment.valid_until.strftime('%Y-%m-%d'),
                         valid_until.strftime('%Y-%m-%d'))

    def test_transaction_done_send_email(self):
        payment, transaction = self._make_transaction(status=1, code="xpto", price="123.54")

        #make sure that the outbox is empty
        mail.outbox = []

        view = NotificationView()
        view.transaction_code = 'xpto'
        view.transaction_done(payment.id)


        #get the created member
        #set the strings to be verified
        body = 'Olá %s! Seu registro na Associação Python Brasil (APyB) já foi realizado!' % self.member.user.get_full_name()
        subject = 'Registro OK'

        #verify the outbox length
        self.assertEqual(len(mail.outbox), 1)
        #verify the subject string
        self.assertEqual(mail.outbox[0].subject, subject)
        #verify the body string
        self.assertEqual(mail.outbox[0].body, body)

    def test_post_with_status_done_should_return_payment_done(self):
        payment, transaction = self._make_transaction(status=1, code="xpto", price='123.45')
        notification_view = NotificationView()
        notification_view.transaction = (lambda code: (3, payment.id, transaction.price))
        request = RequestFactory().post("/", {"notificationCode": "xpto"})

        response = notification_view.post(request)

        transaction = Transaction.objects.get(id=transaction.id)

    def test_post_with_status_available_should_return_payment_done(self):
        payment, transaction = self._make_transaction(
            status=1,
            code="xpto",
            price='123.45',
        )
        notification_view = NotificationView()
        notification_view.transaction = (
            lambda code: (AVAILABLE, payment.id, transaction.price)
        )
        request = RequestFactory().post("/", {"notificationCode": "xpto"})

        response = notification_view.post(request)

        transaction = Transaction.objects.get(id=transaction.id)

        self.assertTrue(payment.done())
        self.assertEqual(b"OK", response.content)

    def test_post_with_other_status_should_not_return_payment_done(self):
        payment, transaction = self._make_transaction(status=1, code="xpto", price='123.45')
        notification_view = NotificationView()
        notification_view.transaction = (lambda code: (7, payment.id, transaction.price))
        request = RequestFactory().post("/", {"notificationCode": "xpto"})

        response = notification_view.post(request)

        transaction = Transaction.objects.get(id=transaction.id)

        self.assertFalse(payment.done())
        self.assertEqual(b"OK", response.content)
