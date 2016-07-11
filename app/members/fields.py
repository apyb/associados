#!/usr/bin/env python
# encoding: utf-8

# """
# From https://github.com/django/django-localflavor/blob/master/localflavor/br/forms.py
# Remove this file when update to newer Django.
# """

# import re
# from django.core.validators import EMPTY_VALUES
# from django.forms import ValidationError
# from django.forms.fields import Field
# from django.utils.translation import ugettext_lazy as _

# try:
#     from django.utils.encoding import smart_text
# except ImportError:
#     from django.utils.encoding import smart_unicode as smart_text


# phone_digits_re = re.compile(r'^(\d{2})[-\.]?(\d{4,5})[-\.]?(\d{4})$')


# class BRPhoneNumberField(Field):
#     """
#     A form field that validates input as a Brazilian phone number, that must
#     be in either of the following formats: XX-XXXX-XXXX or XX-XXXXX-XXXX.
#     """
#     default_error_messages = {
#         'invalid': _(('Phone numbers must be in either of the following '
#                       'formats: XX-XXXX-XXXX or XX-XXXXX-XXXX.')),
#     }

#     def clean(self, value):
#         super(BRPhoneNumberField, self).clean(value)
#         if value in EMPTY_VALUES:
#             return ''
#         value = re.sub('(\(|\)|\s+)', '', smart_text(value))
#         m = phone_digits_re.search(value)
#         if m:
#             return '%s-%s-%s' % (m.group(1), m.group(2), m.group(3))
#         raise ValidationError(self.error_messages['invalid'])
