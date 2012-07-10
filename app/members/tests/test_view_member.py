# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django_dynamic_fixture import G

class MemberListViewTest(TestCase):

    def setUp(self):
        super(MemberListViewTest, self).setUp()
        self._create_user(first_name='test', last_name='test')
        url = reverse('people-members-list')
        self.response = self.client.get(url)

    def test_should_have_a_route(self):
        self.assertEqual(self.response.status_code, 200)

    def test_should_render_the_correctly_template(self):
        templates = [template.name for template in self.response.templates]
        self.assertIn('members/member_list.html', templates)

    def _create_user(self, first_name, last_name, category='1'):
        _user = G(User, first_name=first_name, last_name=last_name)
        _user.member.category=category
        _user.member.save()

    def test_should_render_the_members(self):
        self.assertIn('test test', self.response.rendered_content)
        self.assertIn('Student', self.response.rendered_content)




