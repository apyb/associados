# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django_dynamic_fixture import G


class PeopleTest(TestCase):

    def setUp(self):
        super(PeopleTest, self).setUp()
        user = G(User, first_name='test', last_name='test')
        user.profile.category = 1
        user.profile.save()

        url = reverse('people-members-list')
        self.response = self.client.get(url)

    def test_should_have_a_route(self):
        self.assertEqual(self.response.status_code, 200)

    def test_should_render_the_correctly_template(self):
        templates = [template.name for template in self.response.templates]
        self.assertIn('auth/user_list.html', templates)

    def test_should_render_the_members(self):
        self.assertIn('test test', self.response.rendered_content)
        self.assertIn('Student', self.response.rendered_content)
