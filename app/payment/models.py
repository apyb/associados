# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone

from app.members.models import Member, Category


TRANSACTION_STATUS = (
    ('1', 'Awaiting Payment'),
    ('2', 'In analysis'),
    ('3', 'Paid'),
    ('4', 'Available'),
    ('5', 'In dispute'),
    ('6', 'Returned'),
    ('7', 'Cancelled'),
)


class PaymentType(models.Model):
    category = models.ForeignKey(Category)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    duration = models.IntegerField(help_text='In days', default=1)

    def __unicode__(self):
        return "{0} - {1} for {2} days".format(self.category.name, self.price, self.duration)


class Payment(models.Model):
    member = models.ForeignKey(Member)
    type = models.ForeignKey(PaymentType)
    date = models.DateTimeField(null=True, blank=True)
    code = models.CharField(max_length=50, null=True, blank=True)
    valid_until = models.DateTimeField(null=True, blank=True)
    last_transaction = models.ForeignKey('Transaction', null=True, blank=True, related_name='last_transaction')

    def done(self):
        return self.transaction_set.filter(status=3).exists()

    def __unicode__(self):
        return 'payment from {0}'.format(self.member)


class Transaction(models.Model):
    payment = models.ForeignKey(Payment)
    date = models.DateTimeField(default=timezone.now)
    code = models.CharField(max_length=50)
    status = models.CharField(max_length=1, choices=TRANSACTION_STATUS)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def get_checkout_url(self):
        return settings.PAGSEGURO_WEBCHECKOUT + self.code


def update_payment_transaction(sender, instance, **kwargs):
    payment = instance.payment
    payment.last_transaction = instance
    payment.save()


post_save.connect(receiver=update_payment_transaction, sender=Transaction)
