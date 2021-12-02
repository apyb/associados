

import requests
import logging

from datetime import timedelta
from lxml import html as lhtml

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, \
     HttpResponseBadRequest
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from app.members.models import Member
from app.payment.models import Payment, Transaction

from .payment_service import PaymentService


logger = logging.getLogger(__name__)


class PaymentView(View):
    payment_class = PaymentService

    def _create_payload(self, payment, payment_service):
        payment_service.set_price(payment.type.price)
        payment_service.set_description(
            _('Brazilian Python Association registration payment')
        )
        payment_service.set_reference(payment)

    def set_payment_code(self, payment):
        payment_service = self.get_payment_service()
        self._create_payload(payment, payment_service)
        response = payment_service.post()
        if response.ok:
            dom = lhtml.fromstring(response.content)
            transaction_code = dom.xpath("//code")[0].text
            payment.code = transaction_code
            payment.save()
        return payment

    def get(self, request, member_id):
        member = get_object_or_404(Member, pk=member_id)
        payment_service = self.get_payment_service()
        payment = payment_service.get_member_payment(member)
        payment_with_code = self.set_payment_code(payment)

        if not payment_with_code.code:
            payment_with_code.delete()
            url = '/'
            messages.error(request, _(
                "Failed to generate a transaction within the payment gateway. "
                "Please contact the staff to complete your registration."),
                           fail_silently=True)
        else:
            url = settings.PAYMENT_ENDPOINT_WEBCHECKOUT \
                + payment_with_code.code
        return HttpResponseRedirect(url)

    def get_payment_service(self):
        return self.payment_class()


class NotificationView(View):
    payment_class = PaymentService

    def __init__(self, **kwargs):
        self.transaction_code = None
        super(NotificationView, self).__init__(**kwargs)

    def transaction(self, transaction_code):
        payment_service = self.get_payment_service()

        url_transacao = "%s/%s?email=%s&token=%s" % (
            payment_service.credentials.transactions,
            transaction_code,
            settings.PAYMENT_CREDENTIALS["email"],
            settings.PAYMENT_CREDENTIALS["token"]
        )
        url_notificacao = "%s/%s?email=%s&token=%s" % (
            payment_service.credentials.notifications,
            transaction_code,
            settings.PAYMENT_CREDENTIALS["email"],
            settings.PAYMENT_CREDENTIALS["token"]
        )

        response = requests.get(url_transacao)
        if not response.ok:
            response = requests.get(url_notificacao)
        if response.ok:
            dom = lhtml.fromstring(response.content)
            status_transacao = int(dom.xpath("//status")[0].text)

            referencia = dom.xpath("//reference")[0].text
            try:
                referencia = int(referencia)
            except ValueError:
                logger.error("Incorrect reference: {}".format(referencia))

            valor = float(dom.xpath("//grossamount")[0].text)
            return status_transacao, referencia, valor
        return None, None, None

    def _update_member_category(self, payment):
        member = payment.member
        member.category = payment.type.category
        member.save()

    def _update_payment_dates(self, payment):
        # TODO: we need to think more about this rule and define it...
        payment.valid_until = (
            timezone.now() + timedelta(days=payment.type.duration)
        )
        payment.date = timezone.now()
        payment.save()

    def _send_confirmation_email(self, payment):
        # Send an email confirming the subscription
        user = payment.member.user
        message = ('Olá %s! Seu registro na Associação Python Brasil '
                   '(APyB) já foi realizado!' % user.get_full_name())
        user.email_user('Registro OK', message)

    def transaction_done(self, payment_id):
        payment = Payment.objects.get(id=payment_id)
        self._update_payment_dates(payment)
        self._update_member_category(payment)
        self._send_confirmation_email(payment)

    def create_transaction(self, payment_id, status, price, code):
        Transaction.objects.create(
            payment_id=payment_id,
            code=code,
            status=status,
            price=price
        )

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(NotificationView, self).dispatch(*args, **kwargs)

    def post(self, request):
        self.transaction_code = request.POST.get("notificationCode")
        if self.transaction_code:
            status, payment_id, price = self.transaction(self.transaction_code)

            if status is None or payment_id is None or price is None:
                return HttpResponseBadRequest("Error processing transaction")

            if status == 3:
                self.transaction_done(payment_id)
            self.create_transaction(payment_id, status, price,
                                    self.transaction_code)

        return HttpResponse("OK")

    def get_payment_service(self):
        return self.payment_class()
