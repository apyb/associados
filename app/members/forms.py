#!/usr/bin/env python
# encoding: utf-8
from django import forms
from django.contrib.auth.models import User
from django.contrib.localflavor.br.forms import BRCPFField, BRPhoneNumberField, BRStateSelect
from django.utils.translation import gettext_lazy as _
from app.members.models import City, Organization, Member


class UserForm(forms.ModelForm):
    full_name = forms.CharField(label=_("Name"), required=True)
    email = forms.EmailField(label=_("E-Mail"), required=True)

    class Meta:
        model = User
        fields = ('full_name', 'email')

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name'].split(' ')
        first_name = full_name.pop(0)
        last_name = ' '.join(full_name)
        self.cleaned_data.update({'first_name': first_name})
        self.cleaned_data.update({'last_name': last_name})
        return self.cleaned_data['full_name']

    def save(self, commit=True):
        full_name = self.cleaned_data.get('full_name')
        full_name_list = full_name.split(' ')

        self.instance.username = self.data['cpf']
        self.instance.last_name = full_name_list.pop(-1)
        self.instance.first_name = ' '.join(full_name_list)

        return super(UserForm, self).save(commit)


class UserEditionForm(forms.ModelForm):
    '''
    Este form é redundante, mas do jeito que está o UserForm
    não da pra aproveitar para edição
    Necessário refactory destes forms -  UserForm e UserEditionForm.

    '''
    class Meta:
        model = User
        fields = ('id', 'last_name', 'first_name', 'email')


class MemberForm(forms.ModelForm):
    cpf = BRCPFField(label=_("CPF"), required=True)
    phone = BRPhoneNumberField(label=_("Phone"), required=False)
    organization = forms.CharField(label=_("Organization"))
    city = forms.CharField(label=_("City"))
    state = forms.CharField(label=_("State"), widget=BRStateSelect())

    class Meta:
        model = Member
        exclude = ('user', )
        fields = ('category', 'organization', 'cpf', 'phone', 'address', 'city', 'state', 'relation_with_community', 'mailing', 'partner')

    def clean_organization(self):
        organization =  self.cleaned_data['organization']
        if organization:
            organization_instance, created = Organization.objects.get_or_create(name=organization)
            return organization_instance
        return None

    def clean_city(self):
        city =  self.cleaned_data['city']
        state = self.data.get('state')
        if city:
            city_instance, created = City.objects.get_or_create(name=city, state=state)
            return city_instance
        return None

    def save(self, user, commit=True):
        self.instance.user = user
        return super(MemberForm, self).save(commit)


