# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, UserManager
from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from app.members.models import Member, Category, City, Organization
from django_dynamic_fixture import G


class UserRegisterView(TestCase):
    def setUp(self):
        super(UserRegisterView, self).setUp()

        self.url = reverse('members-signup')

        self.empty_data = {
            u'email': u'',
            u'password1': u'',
            u'password2': u'',
        }

        self.user_data = {
            u'email': u'member@mail.com',
            u'password1': u'password1',
            u'password2': u'password1',
        }

    def test_should_have_a_route(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_should_render_the_correctly_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'members/member_signup.html')

    def test_post_with_blank_fields_should_return_error(self):
        response = self.client.post(self.url, {'email': '', 'password1': '', 'password2': ''})
        self.assertFormError(response, 'form', 'email', u'This field is required.')
        self.assertFormError(response, 'form', 'password1', u'This field is required.')
        self.assertFormError(response, 'form', 'password2', u'This field is required.')

    def test_post_with_correcly_data_should_create_a_user(self):
        self.response = self.client.post(self.url, data=self.user_data)
        try:
            User.objects.get(email=self.user_data['email'])
        except Member.DoesNotExist:
            self.fail("Member does not exist")

    def test_post_with_correcly_data_should_redirect_to_members_form(self):
        self.response = self.client.post(self.url, data=self.user_data)
        members_form_url = reverse('members-form')
        self.assertRedirects(self.response, members_form_url)

