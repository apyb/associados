from django.db import models
from app.members.models import Member, Category


PAYMENT_STATUS = (
    (1, 'waiting'),
    (2, 'approved'),
    (3, 'deny')
)


class PaymentType(models.Model):
    category = models.ForeignKey(Category)
    value = models.FloatField()
    duration = models.IntegerField(help_text='In days')


class Payment(models.Model):
    member = models.ForeignKey(Member)
    payment_date = models.DateField(auto_now_add=True)
    valid_until = models.DateField()
    value = models.FloatField(default=0)
    status = models.IntegerField(choices=PAYMENT_STATUS)
    type = models.OneToOneField(PaymentType)

