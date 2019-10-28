# -*- coding: utf-8 -*-
from datetime import timedelta

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from app.members.models import Category, Member
from app.members.tests.helpers import create_user_with_member
from app.payment.models import Payment, PaymentType

class MemberListViewTest(TestCase):

    def setUp(self):
        category = Category.objects.get(id=2)
        create_user_with_member(first_name='teste', last_name='teste')
        create_user_with_member(first_name='dolor', last_name='sit')
        create_user_with_member(first_name='lorem', last_name='ipsum', category=category)
        create_user_with_member(first_name='amet', last_name='consectetur', category=category)
        create_user_with_member(first_name='python',
                                last_name='long name user',
                                category=category)

        members = [
            Member.objects.filter(user__first_name=name).first()
            for name in ('teste', 'dolor', 'lorem', 'amet', 'python')
        ]

        payment_type = PaymentType.objects.create(
            category=category, price=50.0, duration=10
        )

        for idx, member in enumerate(members):
            date = timezone.now() if idx % 2 == 0 else timezone.now() - timedelta(days=370)
            valid_until=date + timedelta(days=365)
            Payment.objects.create(
                member=member,
                type=payment_type,
                date=date,
                valid_until=valid_until
            )

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
        self.assertNotIn('lorem ipsum', response.rendered_content)
        self.assertNotIn('dolor sit', response.rendered_content)

    def test_should_filter_members(self):
        response = self.client.get(self.url, {
            'category': 1,
        })
        self.assertIn('teste teste', response.rendered_content)
        self.assertNotIn('dolor sit', response.rendered_content)
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

    def test_should_search_by_first_and_last_name(self):
        response = self.client.get(self.url, {
            'q': 'python long name user',
            'category': 1,
        })
        self.assertIn('python long name user', response.rendered_content)
        self.assertNotIn('dolor sit', response.rendered_content)
        self.assertNotIn('lorem ipsum', response.rendered_content)
        self.assertNotIn('amet consectetur', response.rendered_content)
