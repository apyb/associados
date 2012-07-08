# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse

from django.test import TestCase
from app.people.models import UserProfile

from django_dynamic_fixture import G

class PeopleTest(TestCase):

    def setUp(self):
        super(PeopleTest, self).setUp()
        self._create_user(first_name='test', last_name='test')

        url = reverse('people-members-list')
        self.response = self.client.get(url)

    def test_list_view_works(self):
        self.assertEqual(self.response.status_code, 200)

    def test_flatpage_render_custom_template(self):
        templates = [template.name for template in self.response.templates]
        self.assertIn('people/userprofile_list.html', templates)

    def _create_user(self, first_name, last_name, category='1'):
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,

        )
        G(UserProfile, user=user, category=category)

    def test_member_data_are_rendered_in_template(self):
        self.assertIn('test test', self.response.rendered_content)
        self.assertIn('Student', self.response.rendered_content)

