#!/usr/bin/env python
# encoding: utf-8
from django.db import models
from django.utils import timezone
from app.core.models import DefaultFields

from django.contrib.localflavor.br.br_states import STATE_CHOICES
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


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
        return "{0} - {1}".format(self.name, self.state)


class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = _('Categories')

    def __unicode__(self):
        return self.name


class Member(models.Model):
    user = models.OneToOneField(User)
    category = models.ForeignKey(Category, verbose_name=_('Category'))
    organization = models.ForeignKey(Organization, null=True, blank=True)
    cpf = models.CharField(_('CPF'), max_length=11, db_index=True, unique=True)
    phone = models.CharField(_('Phone'), max_length=50, null=True, blank=True)
    address = models.TextField(_('Address'), null=True, blank=True)
    location = models.CharField(_('Location'), max_length=100, null=True, blank=True)
    relation_with_community = models.TextField(_('Relation with community'), null=True, blank=True)
    mailing = models.BooleanField(_('Mailing'), default=True)
    partner = models.BooleanField(_('Partner'), default=True)

    def get_days_to_next_payment(self, payment):
        if payment and payment.done() and payment.valid_until is not None:
            dif = payment.valid_until - timezone.now()
            return dif.days
        return 0

    def get_last_payment(self):
        payments = self.payment_set.filter(last_transaction__status='done').order_by('-date')
        if not payments:
            return None
        return payments.order_by('-date')[0]

    def get_payment_check_list(self):
        last_payment = self.get_last_payment()
        days_left = self.get_days_to_next_payment(last_payment)
        return {
            'expired': days_left <= 0,
            'days_left': days_left,
            'last_payment': last_payment
        }

    def __unicode__(self):
        return self.user.get_full_name()
