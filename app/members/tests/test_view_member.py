# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from app.members.models import Member
from django_dynamic_fixture import G

class MemberListViewTest(TestCase):

    def setUp(self):
        super(MemberListViewTest, self).setUp()
        self._create_user(first_name='test', last_name='test')
        self._create_user(first_name='dolor', last_name='sit')
        self._create_user(first_name='lorem', last_name='ipsum', category=2)
        self._create_user(first_name='amet', last_name='consectetur', category=2)

        self.url = reverse('people-members-list')
        self.response = self.client.get(self.url)

    def test_should_have_a_route(self):
        self.assertEqual(self.response.status_code, 200)

    def test_should_render_the_correctly_template(self):
        self.assertTemplateUsed('members/member_list.html')

    def _create_user(self, first_name, last_name, category='1'):
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username='%s%s' % (first_name, last_name),
        )
        G(Member, user=user, category=category)

    def test_should_render_the_members(self):
        self.assertIn('test test', self.response.rendered_content)
        self.assertIn('Student', self.response.rendered_content)

    def test_should_search_members(self):
        response = self.client.get(self.url, {
            'q': 'te',
        })
        self.assertIn('test test', response.rendered_content)
        self.assertIn('amet consectetur', response.rendered_content)
        self.assertNotIn('dolor sit', response.rendered_content)
        self.assertNotIn('lorem ipsum', response.rendered_content)

    def test_should_filter_members(self):
        response = self.client.get(self.url, {
            'category': 1,
        })
        self.assertIn('test test', response.rendered_content)
        self.assertIn('dolor sit', response.rendered_content)
        self.assertNotIn('lorem ipsum', response.rendered_content)
        self.assertNotIn('amet consectetur', response.rendered_content)

    def test_should_search_and_filter_members(self):
        response = self.client.get(self.url, {
            'q': 'te',
            'category': 1,
        })
        self.assertIn('test test', response.rendered_content)
        self.assertIn('dolor sit', response.rendered_content)
        self.assertNotIn('lorem ipsum', response.rendered_content)
        self.assertNotIn('amet consectetur', response.rendered_content)

class MemberRegisterView(TestCase):
    def setUp(self):
        super(MemberRegisterView, self).setUp()

        url = reverse('people-member-register')
        self.response = self.client.get(url)

    def test_should_have_a_route(self):
        self.assertEqual(self.response.status_code, 200)

    def test_should_render_the_correctly_template(self):
        self.assertTemplateUsed('members/member_register.html')
