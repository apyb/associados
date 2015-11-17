#!/usr/bin/env python
# encoding: utf-8
from django import forms
from django.contrib.auth.models import User
from django.contrib.localflavor.br.forms import BRCPFField
from django.forms import TextInput
from django.forms.util import flatatt

from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import Organization, Member, Category
from .fields import BRPhoneNumberField

class OrganizationInput(TextInput):
    def _format_value(self, value):
        if type(value) is not int:
            return value
        try:
            organization = Organization.objects.get(id=value)
            value = organization.name
        except Organization.DoesNotExist:
            value = ''
        return value

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(self._format_value(value))
        return mark_safe(u'<input%s />' % flatatt(final_attrs))


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
    github_user = forms.CharField(label=_("GitHub User"), required=False)
    organization = forms.CharField(label=_("Organization"), widget=OrganizationInput, required=False)
    location = forms.CharField(label=_("Location"), required=False)

    class Meta:
        model = Member
        exclude = ('user', )
        fields = ('category', 'github_user', 'organization', 'cpf', 'phone', 'address', 'location',
                  'relation_with_community', 'mailing', 'partner')

    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args,**kwargs)
        if self.instance:
            if not self.instance.get_payment_status():
                self.fields['category'].widget.attrs['disabled'] = True

    def clean_category(self):
        category = self.cleaned_data['category']
        if self.instance.id:
            if not self.instance.get_payment_status():
                if self.instance.category != category:
                    raise forms.ValidationError(_("You can't change your category with pending payments"))
        return category

    def clean_organization(self):
        organization = self.cleaned_data['organization']
        if not organization:
            return None
        organization_instance, created = Organization.objects.get_or_create(name=organization)
        return organization_instance

    def save(self, user, commit=True):
        self.instance.user = user
        return super(MemberForm, self).save(commit)
