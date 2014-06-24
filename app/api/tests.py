#coding: utf-8
import json
from datetime import datetime, timedelta

from django.test import TestCase
from django.core.urlresolvers import reverse

from model_mommy import mommy

from app.payment.models import PaymentType

less_than_a_year_ago = datetime.now() - timedelta(days=363)
more_than_a_year_ago = datetime.now() - timedelta(days=366)
two_days_from_now = datetime.now() + timedelta(days=2)
yesterday = datetime.now()


class VerifyMembershipTestCase(TestCase):

    def setUp(self):
        
        user1 = mommy.make('auth.User', email="user1@test.com")
        user2 = mommy.make('auth.User', email="user2@test.com")
        self.active_member = mommy.make('members.Member', user=user1)
        self.inactive_member = mommy.make('members.Member', user=user2)
        payment_type = PaymentType.objects.get(pk=1)  # Efetivo
        self.valid_payment = mommy.make(
            'payment.Payment', member=self.active_member,
            type=payment_type, date=less_than_a_year_ago, valid_until=two_days_from_now)
        self.invalid_payment = mommy.make(
            'payment.Payment', member=self.inactive_member,
            type=payment_type, date=more_than_a_year_ago, valid_until=yesterday)
        self.transaction1 = mommy.make(
            'payment.Transaction', status='4',
            date=less_than_a_year_ago, payment=self.valid_payment)
        self.transaction2 = mommy.make(
            'payment.Transaction', status='4',
            date=more_than_a_year_ago, payment=self.invalid_payment)

    def test_verify_valid_member(self):
        data = {
            'email': "user1@test.com",
            'token': 'PYBR10ROCKS'
        }
        response = self.client.get(reverse('verify-membership'), data)
        status = json.loads(response.content)
        self.assertFalse(status['expired'])

    def test_verify_invalid_member(self):
        data = {
            'email': "user2@test.com",
            'token': 'PYBR10ROCKS'
        }
        response = self.client.get(reverse('verify-membership'), data)
        status = json.loads(response.content)
        self.assertTrue(status['expired'])

    def test_without_token(self):
        data = {
            'email': "user2@test.com",
        }
        response = self.client.get(reverse('verify-membership'), data)
        
        self.assertEqual(response.status_code, 401)

    def test_not_a_member(self):
        data = {
            'email': "another.email@test.com",
            'token': 'PYBR10ROCKS'
        }
        response = self.client.get(reverse('verify-membership'), data)
        
        self.assertEqual(response.status_code, 404)


