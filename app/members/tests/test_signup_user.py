# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _


class MemberSignupView(TestCase):
    def setUp(self):
        self.url = reverse('members-signup')

        self.empty_data = {
            u'email': u'',
            u'password1': u'',
            u'password2': u'',
        }

        self.data = {
            u'email': u'fake_user@fake.com',
            u'password1': u'fake_pass',
            u'password2': u'fake_pass',
        }

    def test_should_have_a_route(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_should_render_the_correctly_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'members/member_signup.html')

    def test_post_with_blank_fields_should_return_error(self):
        self.response = self.client.post(self.url, data=self.empty_data)
        self.assertContains(self.response, _(u'This field is required.'), count=3)

    def test_post_with_correcly_data_should_redirect_to_dashboard(self):
        self.response = self.client.post(self.url, data=self.data)
        dashboard_url = reverse('members-form')

        self.assertEqual(self.response.status_code, 302)
        self.assertTrue(self.response['location'].endswith(dashboard_url))
