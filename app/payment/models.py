from django.conf import settings
from django.db import models
from app.members.models import Member, Category



class PaymentType(models.Model):
    category = models.ForeignKey(Category)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    duration = models.IntegerField(help_text='In days', default=1)

    def __unicode__(self):
        return self.category.name


class Payment(models.Model):
    member = models.ForeignKey(Member)
    type = models.ForeignKey(PaymentType)
    date = models.DateTimeField(null=True, blank=True)
    valid_until = models.DateTimeField(null=True, blank=True)

    def done(self):
        return self.transaction_set.filter(status="done").exists()


class Transaction(models.Model):
    payment = models.ForeignKey(Payment)
    code = models.CharField(max_length=50)
    status = models.CharField(max_length=25)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def get_checkout_url(self):
        return settings.PAGSEGURO_WEBCHECKOUT + self.code

