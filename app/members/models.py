# coding: utf-8

import requests
import slumber

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from localflavor.br.br_states import STATE_CHOICES
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from app.core.models import DefaultFields
from django_gravatar.helpers import get_gravatar_url
from app.members.mail import send_email


github_api = slumber.API("https://api.github.com/", append_slash=False)


class Organization(DefaultFields):
    name = models.CharField(_('Name'), max_length=250)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = _('Organizations')

    def __str__(self):
        return self.name


class City(DefaultFields):
    state = models.CharField(_('State'), max_length=2, choices=STATE_CHOICES)
    name = models.CharField(_('Name'), max_length=250)

    class Meta:
        ordering = ('state', 'name')
        verbose_name_plural = _('Cities')

    def __str__(self):
        return u"{0} - {1}".format(self.name, self.state)


class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name


class Member(models.Model):
    user = models.OneToOneField(User)
    category = models.ForeignKey(Category, verbose_name=_('Category'))
    github_user = models.CharField(
        _('Github User'), max_length=50, null=True, blank=True)
    organization = models.ForeignKey(Organization, null=True, blank=True)
    cpf = models.CharField(_('CPF'), max_length=11, db_index=True, unique=True)
    phone = models.CharField(_('Phone'), max_length=50, null=True, blank=True)
    address = models.TextField(_('Address'), null=True, blank=True)
    location = models.CharField(
        _('Location'), max_length=100, null=True, blank=True)
    relation_with_community = models.TextField(
        _('Relation with community'), null=True, blank=True)
    mailing = models.BooleanField(_('Mailing'), default=True)
    partner = models.BooleanField(_('Partner'), default=True)

    diretoria = models.NullBooleanField('Diretoria', default=False, null=True)
    thumb_image = models.CharField(
        'Thumbimage', max_length=100, null=True, blank=True)
    municipio = models.ForeignKey('municipios.Municipio',
                                  verbose_name=u"Município",
                                  related_name="municipio_org_mun",
                                  null=True, blank=True)

    def change_category(self):
        self.category = Category.objects.get(name="Efetivo")
        self.save()
        return True

    def get_days_to_next_payment(self, payment):
        if payment and payment.done() and payment.valid_until is not None:
            dif = payment.valid_until - timezone.now()
            return dif.days
        return 0

    def get_first_payment(self):
        payments = self.payment_set.filter(
            last_transaction__status__in=[3, 4]).order_by('date')
        if not payments:
            return None
        return payments[0]

    def get_last_payment(self):
        payments = self.payment_set.filter(
            last_transaction__status__in=[3, 4]).order_by('-date')
        if not payments:
            return None
        return payments[0]

    def get_payment_status(self):
        if not self.id:
            return True

        last_payment = self.get_last_payment()
        days_left = self.get_days_to_next_payment(last_payment)
        return days_left > 1

    def get_payment_check_list(self):
        first_payment = self.get_first_payment()
        last_payment = self.get_last_payment()
        days_left = self.get_days_to_next_payment(last_payment)
        return {
            'expired': days_left <= 0,
            'days_left': days_left,
            'last_payment': last_payment,
            'first_payment': first_payment,
        }

    @property
    def github(self):
        if not self.github_user:
            return None
        try:
            return github_api.users(self.github_user).get(client_id=settings.GITHUB_CLIENT_ID,
                                                          client_secret=settings.GITHUB_CLIENT_SECRET)
        except slumber.exceptions.HttpClientError:
            return None
        except slumber.exceptions.HttpServerError:
            return None
        except requests.ConnectionError:
            return None

    @property
    def update_thumbnail(self):
        try:
            g = self.github
            if g:
                self.thumb_image = g["avatar_url"]
            else:
                self.thumb_image = get_gravatar_url(self.user.email, size=150)
            self.save()
        except Exception as e:
            raise e
        return self.thumb_image

    def full_name(self):
        return self.user.get_full_name() or self.user.username

    def __str__(self):
        return self.full_name()


@receiver(post_save, sender=Member)
def sending_email(sender, instance, created, **kwargs):
    if created:
        send_email(subject="Bem vindo a Assosiação PythonBrasil",
                   template_name='members/email.html',
                   context=instance.user.first_name,
                   recipient_list=[instance.user.email])
