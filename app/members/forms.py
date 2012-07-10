#!/usr/bin/env python
# encoding: utf-8
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.contrib.localflavor.br.forms import BRCPFField, BRPhoneNumberField, BRStateSelect
from app.members.models import City, Organization


class MemberForm(forms.ModelForm):
    full_name = forms.CharField()
    organization = forms.CharField()
    cpf = BRCPFField()
    email = forms.EmailField()
    phone = BRPhoneNumberField(required=False)
    address = forms.CharField(widget=forms.Textarea(attrs={'style': 'width:70%'}), required=False)
    city = forms.CharField(required=False)
    state = forms.CharField(widget=BRStateSelect())
    public_key = forms.FileField(required=False)
    category = forms.ChoiceField(choices=((1, _('Student')), (2, _('Member'))))
    relationship = forms.CharField(widget=forms.Textarea(attrs={'style': 'width:70%'}), required=False)
    mailling = forms.BooleanField(widget=forms.CheckboxInput(attrs={'checked': 'checked'}), required=False)
    contact = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ()

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name'].split(' ')
        first_name = full_name.pop(0)
        last_name = ' '.join(full_name)
        self.cleaned_data.update({'first_name': first_name})
        self.cleaned_data.update({'last_name': last_name})
        return self.cleaned_data['full_name']

    def clean(self):
        data = self.cleaned_data
        city, _ = City.objects.get_or_create(name=data.get('city'), state=data.get('state'))
        organization, _ = Organization.objects.get_or_create(name=data.get('organization'))
        data['city'] = city
        data['organization'] = organization
        return data

    def save(self):
        data = self.cleaned_data
        self.instance.username = data.get('full_name').replace(' ', '').lower()
        self.instance.first_name = data.get('first_name')
        self.instance.last_name = data.get('last_name')
        self.instance.email = data.get('email')
        user = super(MemberForm, self).save()

        user.member.phone = data.get('phone')
        user.member.address = data.get('address')
        user.member.organization = data.get('organization')
        user.member.city = data.get('city')
        user.member.public_key = data.get('public_key')
        user.member.category = data.get('category')
        user.member.realationship = data.get('relationship')
        user.member.mailling = data.get('mailling')
        user.member.contact = data.get('contact')
        user.member.save()

        return user
