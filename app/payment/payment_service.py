import requests
from django.conf import settings
from .models import PaymentType, Payment


class PagSeguroCredentials(object):

    PRICE_PAYLOAD_ATTRIBUTE = "itemAmount1"
    DESCRIPTION_PAYLOAD_ATTRIBUTE = "itemDescription1"
    REFERENCE_ATTRIBUTE = "reference"

    def __init__(self):

        PAYMENT_ENDPOINT_BASE = settings.PAYMENT_CREDENTIALS_BASE
        PAYMENT_ENDPOINT_WEBCHECKOUT = (
            settings.PAYMENT_ENDPOINT_WEBCHECKOUT
        )
        PAYMENT_ENDPOINT_PRE_APPROVAL = (
            '%s/pre-approvals/request' % PAYMENT_ENDPOINT_BASE
        )

        self.pre_approval = '%s/pre-approvals/request' \
            % PAYMENT_ENDPOINT_BASE
        self.checkout = '%s/checkout' % PAYMENT_ENDPOINT_BASE
        self.transactions = '%s/transactions' % PAYMENT_ENDPOINT_BASE
        self.notifications = '%s/notifications' % self.transactions
        self.web_checkout = PAYMENT_ENDPOINT_WEBCHECKOUT
        self.pre_approval = PAYMENT_ENDPOINT_PRE_APPROVAL
        self.web_pre_approval = settings.PAYMENT_ENDPOINT_WEB_PRE_APPROVAL


class PaymentService(object):

    def __init__(self, PAYMENT_SYSTEM=None, PAYMENT_CREDENTIALS=None):
        self.payment_system = PAYMENT_SYSTEM or settings.PAYMENT_SYSTEM
        self._set_payment_system()
        self.payload = settings.PAYMENT_CREDENTIALS

    def set_price(self, price):
        self.payload[
            self.credentials.PRICE_PAYLOAD_ATTRIBUTE
        ] = "%.2f" % price

    def set_description(self, description):
        self.payload[
            self.credentials.DESCRIPTION_PAYLOAD_ATTRIBUTE
        ] = description

    def set_reference(self, payment):
        self.payload[
            self.credentials.REFERENCE_ATTRIBUTE
        ] = "%d" % payment.pk

    def _set_payment_system(self):
        if self.payment_system != 'PAGSEGURO':
            return
        self.credentials = PagSeguroCredentials()

    def post(self):
        self._set_headers()
        return requests.post(self.credentials.checkout, data=self.payload,
                             headers=self.headers)

    @classmethod
    def get_member_payment(cls, member):
        payment = Payment.objects.filter(
            member=member,
            type__category=member.category,
            transaction__isnull=False,
        ).last()

        if payment is None:
            payment_type = PaymentType.objects.get(category=member.category)
            payment = Payment.objects.create(
                member=member,
                type=payment_type,
            )

        return payment

    def _set_headers(self):
        self.headers = {"Content-Type":
                        "application/x-www-form-urlencoded; charset=UTF-8"}
