#!/usr/bin/env python
# encoding: utf-8
from django.db import models
from app.core.models import DefaultFields

from django.contrib.localflavor.br.br_states import STATE_CHOICES
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from datetime import datetime


class Organization(DefaultFields):
    name = models.CharField(_('Name'), max_length=250)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = _('Organizations')

    def __unicode__(self):
        return self.name


class City(DefaultFields):
    state = models.CharField(_('State'), max_length=2, choices=STATE_CHOICES)
    name = models.CharField(_('Name'), max_length=250)

    class Meta:
        ordering = ('state', 'name')
        verbose_name_plural = _('Cities')

    def __unicode__(self):
        return self.name


def get_public_key_storage_path(instance, filename):
        return 'public_key/%s/%s' % (instance.pk, filename)


class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = _('Categories')

    def __unicode__(self):
        return self.name


class Member(models.Model):
    user = models.OneToOneField(User)
    #TODO: this field must be removes in favor of Category Model
    category = models.ForeignKey(Category)
    organization = models.ForeignKey(Organization, null=True, blank=True)
    cpf = models.CharField(_('CPF'), max_length=11, db_index=True, unique=True)
    phone = models.CharField(_('Phone'), max_length=50, null=True, blank=True)
    address = models.TextField(_('Address'), null=True, blank=True)
    city = models.ForeignKey(City, db_index=True)
    public_key = models.FileField(_('Public Key'), upload_to=get_public_key_storage_path,
                                  null=True, blank=True)
    relation_with_community = models.TextField(_('Relation with community'), null=True, blank=True)
    mailing = models.BooleanField(_('Mailing'), default=True)
    partner = models.BooleanField(_('Partner'), default=True)

    def get_category(self):
        raise NotImplementedError

    def make_payment(self):
        raise NotImplementedError

    def get_payment_check_list(self):
        '''
        expired = True para pagamentos reazalidos até 1 ano (365 dias) atrás  
        expired = False para todas as outroas condições
        days_left = int(n) dias que faltam para vencer o pagamento / negativo (-n) se expirado.
        last_date = data do ultimo pagamento  - "None" se nenhum foi realizado.
        '''
        payment_valid = False
        days_left = None
        payments = self.payment_set.all().order_by('-date')
        if payments:
            last_payment = self.payment_set.all().order_by('-date')[0]
            if last_payment.valid_until is not None:
                dif = last_payment.valid_until - datetime.now()
                if dif.days > 0:
                    payment_valid = True
                days_left = dif.days
        return {'expired': not payment_valid, 'days_left': days_left, 'last_date': None}

    def __unicode__(self):
        return self.user.get_full_name()
