# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.utils import timezone
import requests

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse

from django.utils.decorators import method_decorator
from django.utils.translation import ugettext
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from lxml import html as lhtml

from app.members.models import Member
from app.payment.models import Payment, Transaction, PaymentType


class PaymentView(View):

    def _create_payload(self, payment):
        payload = settings.PAGSEGURO
        price = payment.type.price
        payload["itemAmount1"] = "%.2f" % price
        payload['itemDescription1'] = ugettext(u'Brazilian Python Association registration payment')
        payload["reference"] = "%d" % payment.pk
        return payload, price

    def generate_transaction(self, payment):
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        payload, price = self._create_payload(payment)
        response = requests.post(settings.PAGSEGURO_CHECKOUT, data=payload, headers=headers)
        if response.ok:
            dom = lhtml.fromstring(response.content)
            transaction_code = dom.xpath("//code")[0].text

            transaction = Transaction.objects.create(
                payment=payment,
                code=transaction_code,
                status=1,
                price=price
            )
            return transaction
        return Transaction.objects.none()

    def get(self, request, member_id):
        member = Member.objects.get(id=member_id)
        payment_type = PaymentType.objects.get(category=member.category)
        payment = Payment.objects.create(
            member=member,
            type=payment_type
        )
        t = self.generate_transaction(payment)

        if not t:
            payment.delete()
            url = '/'
            messages.error(request, ugettext("Failed to generate a transaction within the payment gateway. Please contact the staff to complete your registration."), fail_silently=True)
        else:
            url = settings.PAGSEGURO_WEBCHECKOUT + t.code
        return HttpResponseRedirect(url)


class NotificationView(View):

    def __init__(self, **kwargs):
        self.transaction_code = None
        self.methods_by_status = {
            3: self.transaction_done,
            7: self.transaction_canceled,
        }
        super(NotificationView, self).__init__(**kwargs)

    def transaction(self, transaction_code):
        url_transacao = "%s/%s?email=%s&token=%s" % (
            settings.PAGSEGURO_TRANSACTIONS,
            transaction_code,
            settings.PAGSEGURO["email"],
            settings.PAGSEGURO["token"]
        )
        url_notificacao = "%s/%s?email=%s&token=%s" % (
            settings.PAGSEGURO_TRANSACTIONS_NOTIFICATIONS,
            transaction_code,
            settings.PAGSEGURO["email"],
            settings.PAGSEGURO["token"]
        )

        response = requests.get(url_transacao)
        if not response.ok:
            response = requests.get(url_notificacao)
        if response.ok:
            dom = lhtml.fromstring(response.content)
            status_transacao = int(dom.xpath("//status")[0].text)
            referencia = int(dom.xpath("//reference")[0].text)
            valor = float(dom.xpath("//grossamount")[0].text)
            return status_transacao, referencia, valor
        return None, None

    def _update_member_category(self, payment):
        member = payment.member
        member.category = payment.type.category
        member.save()

    def _update_payment_dates(self, payment):
        last_payment = payment.member.get_last_payment()
        if last_payment:
            payment.valid_until = last_payment.valid_until + timedelta(days=payment.type.duration)
        else:
            payment.valid_until = datetime.now(tz=timezone.get_default_timezone()) \
                                  + timedelta(days=payment.type.duration)

        payment.date = datetime.now(tz=timezone.get_default_timezone())
        payment.save()

    def _send_confirmation_email(self, payment):
        #Send an email confirming the subscription
        user = payment.member.user
        message = u'Olá %s! Seu registro na Associação Python Brasil (APyB) já foi realizado!' % user.get_full_name()
        user.email_user(u'Registro OK', message)

    def transaction_done(self, payment_id):
        payment = Payment.objects.get(id=payment_id)
        self._update_payment_dates(payment)
        self._update_member_category(payment)
        self._send_confirmation_email(payment)

        transaction = Transaction.objects.get(code=self.transaction_code, payment_id=payment_id)
        transaction.status = 3
        transaction.save()

    def transaction_canceled(self, payment_id):
        transaction = Transaction.objects.get(code=self.transaction_code, payment_id=payment_id)
        transaction.status = 7
        transaction.save()

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(NotificationView, self).dispatch(*args, **kwargs)

    def post(self, request):
        self.transaction_code = request.POST.get("notificationCode")

        if self.transaction_code:
            status, payment_id, price = self.transaction(self.transaction_code)
            method = self.methods_by_status.get(status)

            if method:
                method(payment_id)

        return HttpResponse("OK")
