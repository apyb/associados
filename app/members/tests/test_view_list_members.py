# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from app.members.models import Category
from app.members.tests.helpers import create_user_with_member


class MemberListViewTest(TestCase):

    def setUp(self):
        category = Category.objects.get(id=2)
        create_user_with_member(first_name='teste', last_name='teste')
        create_user_with_member(first_name='dolor', last_name='sit')
        create_user_with_member(first_name='lorem', last_name='ipsum', category=category)
        create_user_with_member(first_name='amet', last_name='consectetur', category=category)

        self.url = reverse('members-list')
        self.response = self.client.get(self.url)

    def test_should_have_a_route(self):
        self.assertEqual(self.response.status_code, 200)

    def test_should_render_the_correctly_template(self):
        self.assertTemplateUsed(self.response, 'members/member_list.html')

    def test_should_render_the_members(self):
        self.assertIn('teste teste', self.response.rendered_content)
        self.assertIn('Estudante', self.response.rendered_content)

    def test_should_search_members(self):
        response = self.client.get(self.url, {
            'q': 'te',
        })
        self.assertIn('teste teste', response.rendered_content)
        self.assertIn('amet consectetur', response.rendered_content)
        self.assertNotIn('dolor sit', response.rendered_content)
        self.assertNotIn('lorem ipsum', response.rendered_content)

    def test_should_filter_members(self):


        response = self.client.get(self.url, {
            'category': 1,
        })
        self.assertIn('teste teste', response.rendered_content)
        self.assertIn('dolor sit', response.rendered_content)
        self.assertNotIn('lorem ipsum', response.rendered_content)
        self.assertNotIn('amet consectetur', response.rendered_content)

    def test_should_search_and_filter_members(self):
        response = self.client.get(self.url, {
            'q': 'te',
            'category': 1,
        })
        self.assertIn('teste teste', response.rendered_content)
        self.assertNotIn('dolor sit', response.rendered_content)
        self.assertNotIn('lorem ipsum', response.rendered_content)
        self.assertNotIn('amet consectetur', response.rendered_content)
