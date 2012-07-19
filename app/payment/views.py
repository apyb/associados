# -*- coding: utf-8 -*-
import requests

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse

from django.utils.decorators import method_decorator
from django.utils.translation import ugettext
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from lxml import html as lhtml

from app.members.models import Member
from app.payment.models import Payment, Transaction, PaymentType


class PaymentView(View):

    def generate_transaction(self, payment):
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        payload = settings.PAGSEGURO
        member = payment.member
        price = 0
        payload["itemAmount1"] = "%.2f" % price
        payload['itemDescription1'] = ugettext(u'Payment of the registration no APyB')
        payload["reference"] = "%d" % payment.pk
        response = requests.post(settings.PAGSEGURO_CHECKOUT, data=payload, headers=headers)
        if response.ok:
            dom = lhtml.fromstring(response.content)
            transaction_code = dom.xpath("//code")[0].text

            transaction = Transaction.objects.create(
                payment=payment,
                code=transaction_code,
                status='pending',
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
            messages.error(request, ugettext("Failed to generate a transaction within the payment gateway. Please contact the event staff to complete your registration."), fail_silently=True)
        else:
            url = settings.PAGSEGURO_WEBCHECKOUT + t.code
        return HttpResponseRedirect(url)

    

class NotificationView(View):

    def __init__(self, **kwargs):
        self.methods_by_status = {
            3: self.transaction_done,
            7: self.transaction_canceled,
            }
        super(NotificationView, self).__init__(**kwargs)

    def transaction(self, transaction_code):
        url_transacao = "%s/%s?email=%s&token=%s" % (settings.PAGSEGURO_TRANSACTIONS,
                                                     transaction_code,
                                                     settings.PAGSEGURO["email"],
                                                     settings.PAGSEGURO["token"])
        url_notificacao = "%s/%s?email=%s&token=%s" % (settings.PAGSEGURO_TRANSACTIONS_NOTIFICATIONS, transaction_code, settings.PAGSEGURO["email"], settings.PAGSEGURO["token"])

        response = requests.get(url_transacao)
        if not response.ok:
            response = requests.get(url_notificacao)
        if response.ok:
            dom = lhtml.fromstring(response.content)
            status_transacao = int(dom.xpath("//status")[0].text)
            referencia = int(dom.xpath("//reference")[0].text)
            return status_transacao, referencia
        return None, None

    def _update_member_category(self, payment):
        member = payment.member
        member.category = payment.type.category
        member.save()

    def transaction_done(self, payment_id):
        payment = Payment.objects.get(id=payment_id)

        transaction = Transaction.objects.get(payment=payment)
        transaction.status = "done"
        transaction.save()

        self._update_member_category(payment)



    def transaction_canceled(self, payment_id):
        transaction = Transaction.objects.get(payment_id=payment_id)
        transaction.status = "canceled"
        transaction.save()

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(NotificationView, self).dispatch(*args, **kwargs)

    def post(self, request):
        notification_code = request.POST.get("notificationCode")

        if notification_code:
            status, payment_id = self.transaction(notification_code)
            method = self.methods_by_status.get(status)

            if method:
                method(payment_id)

        return HttpResponse("OK")
