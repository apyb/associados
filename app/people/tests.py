# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

from django.test import TestCase


class PeopleTest(TestCase):

    def setUp(self):
        super(PeopleTest, self).setUp()
        url = reverse('people-members-list')
        self.response = self.client.get(url)

    def test_list_view_works(self):
        self.assertEqual(self.response.status_code, 200)

    def test_flatpage_render_custom_template(self):
        templates = [template.name for template in self.response.templates]
        self.assertIn('people/userprofile_list.html', templates)