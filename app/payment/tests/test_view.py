# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import RequestFactory
from django_dynamic_fixture import G
from app.members.models import Member, Category

from app.payment import views
from app.payment.models import Payment, Transaction, PaymentType
from app.payment.views import PaymentView, NotificationView
from django.core import mail


class MemberTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="Wolverine")
        self.member = G(Member,
            user=self.user,
            category=Category.objects.get(id=1))


class PaymentViewTestCase(MemberTestCase):

    @classmethod
    def setUpClass(cls):
        call_command("loaddata", "profiles.json", verbosity=0)

    @classmethod
    def tearDownClass(cls):
        call_command("flush", interactive=False, verbosity=0)

    def setUp(self):
        super(PaymentViewTestCase, self).setUp()

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
        expected_url = settings.PAGSEGURO_WEBCHECKOUT + "xpto123"
        self.assertEqual(expected_url, response["Location"])

    def test_payment_view_should_create_a_transaction_for_the_user_type(self):
        PaymentView.as_view()(self.request, self.member.id)
        transaction = Transaction.objects.get(payment__member=self.member)
        self.assertEqual(transaction.payment.type.category, self.member.category)

    def test_payment_view_should_create_a_payment_for_the_user_type(self):
        PaymentView.as_view()(self.request, self.member.id)
        transaction = Transaction.objects.get(payment__member=self.member)
        self.assertEqual(transaction.payment.type.price, transaction.price)


    def test_generate_transaction(self):
        payment = Payment.objects.create(
            member=self.member,
            type=PaymentType.objects.get(id=1)
        )
        transaction = PaymentView().generate_transaction(payment)
        self.assertEqual(payment, transaction.payment)
        self.assertEqual("xpto123", transaction.code)




class NotificationViewTestCase(MemberTestCase):

    @classmethod
    def setUpClass(cls):
        call_command("loaddata", "profiles.json", verbosity=0)

    @classmethod
    def tearDownClass(cls):
        call_command("flush", interactive=False, verbosity=0)

    def setUp(self):
        super(NotificationViewTestCase, self).setUp()

        self.user = User.objects.get(pk=1)
        self.requests_original = views.requests

        class ResponseMock(object):
            content = "<xml><status>3</status><reference>3</reference></xml>"

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
            reverse('payment-notification')
        except NoReverseMatch:
            self.fail("Reversal of url named 'notification' failed with NoReverseMatch")

    def test_transaction_should_get_info_about_transaction(self):
        status, ref = NotificationView().transaction("code")
        self.assertEqual(3, status)
        self.assertEqual(3, ref)

    def test_transaction_done(self):
        payment, transaction = self._make_transaction(status="pending", code="xpto", price="123.54")

        NotificationView().transaction_done(payment.id)
        transaction = Transaction.objects.get(id=transaction.id)
        self.assertEqual("done", transaction.status)

    def test_transaction_done_update_member_category(self):
        payment, transaction = self._make_transaction(status="pending", code="xpto", price="123.54")
        NotificationView().transaction_done(payment.id)
        reloaded_member = Member.objects.get(id=self.member.id)
        self.assertEqual(reloaded_member.category, payment.type.category)

    def test_transaction_done_fill_payment_date(self):
        payment, transaction = self._make_transaction(status="pending", code="xpto", price="123.54")
        self.assertFalse(payment.date)
        NotificationView().transaction_done(payment.id)

        reloaded_payment = Payment.objects.get(id=payment.id)
        self.assertTrue(reloaded_payment.date)
        self.assertEqual(reloaded_payment.date.strftime('%Y-%m-%d+%H:%M'),
                         datetime.now().strftime('%Y-%m-%d+%H:%M'))

    def test_transaction_done_fill_payment_valid_until(self):
        payment, transaction = self._make_transaction(status="pending", code="xpto", price="123.54")
        self.assertFalse(payment.valid_until)
        NotificationView().transaction_done(payment.id)

        valid_until = datetime.now() + timedelta(days=payment.type.duration)
        reloaded_payment = Payment.objects.get(id=payment.id)
        self.assertTrue(reloaded_payment.valid_until)
        self.assertEqual(reloaded_payment.valid_until.strftime('%Y-%m-%d+%H:%M'),
                         valid_until.strftime('%Y-%m-%d+%H:%M'))

    def test_transaction_done_send_email(self):
        payment, transaction = self._make_transaction(status="pending", code="xpto", price="123.54")

        #make sure that the outbox is empty
        mail.outbox = []

        NotificationView().transaction_done(payment.id)

        #get the created member
        #set the strings to be verified
        body = u'Olá %s! Seu registro na Associação Python Brasil (APyB) já foi realizado!' % self.member.user.get_full_name()
        subject = u'Registro OK'

        #verify the outbox length
        self.assertEqual(len(mail.outbox), 1)
        #verify the subject string
        self.assertEqual(mail.outbox[0].subject, subject)
        #verify the body string

        self.assertEqual(mail.outbox[0].body, body)



    def test_transaction_canceled(self):
        payment, transaction = self._make_transaction(status="pending", code="xpto", price="115.84")

        NotificationView().transaction_canceled(payment.id)
        transaction = Transaction.objects.get(id=transaction.id)
        self.assertEqual("canceled", transaction.status)

    def test_methods_by_status(self):
        methods_by_status = NotificationView().methods_by_status
        self.assertEqual("transaction_done", methods_by_status[3].__name__)
        self.assertEqual("transaction_canceled", methods_by_status[7].__name__)

    def test_post(self):
        payment, transaction = self._make_transaction(status="pending", code="xpto", price='123.45')
        notification_view = NotificationView()
        notification_view.transaction = (lambda code: (3, 1))
        request = RequestFactory().post("/", {"notificationCode": "123"})

        response = notification_view.post(request)

        transaction = Transaction.objects.get(id=transaction.id)
        self.assertEqual("done", transaction.status)
        self.assertEqual("OK", response.content)
