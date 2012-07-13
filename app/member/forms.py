#!/usr/bin/env python
# encoding: utf-8
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.contrib.localflavor.br.forms import BRCPFField, BRPhoneNumberField, BRStateSelect
from app.member.models import City, Organization, Member


class UserForm(forms.ModelForm):
    full_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

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

        self.instance.username = self.instance.email
        self.instance.last_name = full_name_list.pop(-1)
        self.instance.first_name = ' '.join(full_name_list)

        return super(UserForm, self).save(commit)


class MemberForm(forms.ModelForm):
    phone = BRPhoneNumberField(required=False)
    state = forms.CharField(widget=BRStateSelect())
    organization = forms.CharField()
    city = forms.CharField()

    class Meta:
        model = Member
        exclude = ('user', )

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


#    def save(self, user):
#        member = super(MemberForm, self).save()
#        return member
