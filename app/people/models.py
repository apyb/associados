#!/usr/bin/env python
# encoding: utf-8
from django.db import models
from app.core.models import DefaultFields
from django.contrib.localflavor.br.br_states import STATE_CHOICES
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Organization(DefaultFields):
    name = models.CharField(_('Name'), max_length=250)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class City(DefaultFields):
    state = models.CharField(_('State'), max_length=2, choices=STATE_CHOICES)
    name = models.CharField(_('Name'), max_length=250)

    class Meta:
        ordering = ('state', 'name')

    def __unicode(self):
        return self.name


def get_public_key_storage_path(instance, filename):
        return '%s/public_key/%Y/%m/%d/%s/' % (settings.MEDIA_ROOT, instance.pk)


class UserProfile(DefaultFields):
    CATEGORY_CHOICE = (('1', _('Student')),
                       ('2', _('Member')))

    user = models.OneToOneField(User)
    organization = models.ForeignKey(Organization, null=True, blank=True)
    cpf = models.CharField(_('CPF'), max_length=11, db_index=True)
    fone = models.CharField(_('Fone'), max_length=50, null=True, blank=True)
    address = models.TextField(_('Address'), null=True, blank=True)
    city = models.ForeignKey(City, db_index=True)
    public_key = models.FileField(_('Public Key'), upload_to=get_public_key_storage_path,
                                  null=True, blank=True)
    category = models.CharField(_('Category'), max_length=1, choices=CATEGORY_CHOICE,
                                db_index=True)
    relation_with_community = models.TextField(_('Relation with community'), null=True, blank=True)
    malling = models.BooleanField(_('Malling'), default=True)
    partner = models.BooleanField(_('Partner'), default=True)


