#!/usr/bin/env python
# encoding: utf-8
from django import forms
from django.contrib.auth.models import User
from django.contrib.localflavor.br.forms import BRCPFField, BRPhoneNumberField, BRStateSelect
from django.utils.translation import gettext_lazy as _
from app.members.models import City, Organization, Member


class UserForm(forms.ModelForm):
    first_name = forms.CharField(label=_("First Name"))
    last_name = forms.CharField(label=_("Last Name"))
    email = forms.CharField(label=_("Email"))

    class Meta:
        model = User
        exclude = ('username', )
        fields = ('first_name', 'last_name', 'email')


class MemberForm(forms.ModelForm):
    cpf = BRCPFField(label=_("CPF"), required=True)
    phone = BRPhoneNumberField(label=_("Phone"), required=False)
    organization = forms.CharField(label=_("Organization"))
    location = forms.CharField(label=_("Location"))

    class Meta:
        model = Member
        exclude = ('user', )
        fields = ('category', 'organization', 'cpf', 'phone', 'address', 'location',
                  'relation_with_community', 'mailing', 'partner')

    def clean_organization(self):
        organization = self.cleaned_data['organization']
        if not organization:
            return None
        organization_instance, created = Organization.objects.get_or_create(name=organization)
        return organization_instance

    def save(self, user, commit=True):
        self.instance.user = user
        return super(MemberForm, self).save(commit)
