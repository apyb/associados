
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone

from app.members.models import Member, Category


PAID = '3'
AVALIABLE = '4'


TRANSACTION_STATUS = (
    ('1', 'Awaiting Payment'),
    ('2', 'In analysis'),
    (PAID, 'Paid'),
    (AVALIABLE, 'Available'),
    ('5', 'In dispute'),
    ('6', 'Returned'),
    ('7', 'Cancelled'),
)


class PaymentType(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    duration = models.IntegerField(help_text='In days', default=1)

    def __str__(self):
        return "{0} - {1} for {2} days".format(self.category.name, self.price, self.duration)


class Payment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    type = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True, blank=True)
    code = models.CharField(max_length=50, null=True, blank=True)
    valid_until = models.DateTimeField(null=True, blank=True)
    last_transaction = models.ForeignKey(
        'Transaction',
        null=True,
        blank=True,
        related_name='last_transaction',
        on_delete=models.CASCADE
    )

    def done(self):
        return self.transaction_set.filter(
            status__in=[PAID, AVALIABLE]
        ).exists()

    def __str__(self):
        return 'payment from {0}'.format(self.member)


class Transaction(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    code = models.CharField(max_length=50)
    status = models.CharField(max_length=1, choices=TRANSACTION_STATUS)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def get_checkout_url(self):
        return settings.PAYMENT_ENDPOINT_WEBCHECKOUT + self.code

    @property
    def status_display(self):
        return dict(TRANSACTION_STATUS).get(self.status, "Unknown")

    def __str__(self):
        return "{self.date} - {self.status_display} - {self.price:.2f}".format(self=self)


def update_payment_transaction(sender, instance, **kwargs):
    payment = instance.payment
    payment.last_transaction = instance
    payment.save()


post_save.connect(receiver=update_payment_transaction, sender=Transaction)
