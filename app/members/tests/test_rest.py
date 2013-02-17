#!/usr/bin/env python
# coding: utf-8
from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
from app.members.tests.helpers import create_user_with_member
from app.payment.models import Payment, PaymentType, Transaction
import json


class REST(TestCase):

    def setUp(self):
        super(REST, self).setUp()

        self.url = reverse('members-status')

        # Active member
        self.user_valid = create_user_with_member(
            first_name='active',
            email='active@test.com',
        )
        self.member_valid = self.user_valid.member
        payment_type = PaymentType.objects.create(
            category=self.member_valid.category,
            price=50.0,
            duration=10
        )
        self.payment = Payment.objects.create(
            member=self.member_valid,
            type=payment_type,
            date=timezone.now(),
            valid_until=timezone.now() + timedelta(days=10, minutes=1)
        )
        self.transaction = Transaction.objects.create(
            payment=self.payment,
            code='fake-code',
            status=3,
            price=50.0
        )

        # Inactive member
        self.user_invalid = create_user_with_member(
            first_name='inactive',
            email='inactive@test.com',
        )

    def test_should_have_a_route(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_should_receive_error_json(self):
        request = self.client.get(self.url)
        response = json.loads(request.content)
        expected = {u"error": u"Could not find any valid parameters. Options: ['email', 'cpf']"}

        self.assertEqual(response, expected)

    def test_should_find_active_user(self):
        """Tests using the search parameters to find an 'active' member"""
        params = {
            'url': self.url,
            'email': 'active@test.com',
            'cpf': self.user_valid.member.cpf
        }

        request = self.client.get("%(url)s?cpf=%(cpf)s&email=%(email)s" % (params))
        response = json.loads(request.content)
        expected = {u'status': u'active'}
        self.assertEqual(response, expected)

        request = self.client.get("%(url)s?email=%(email)s" % (params))
        response = json.loads(request.content)
        expected = {u'status': u'active'}
        self.assertEqual(response, expected)

        request = self.client.get("%(url)s?cpf=%(cpf)s" % (params))
        response = json.loads(request.content)
        expected = {u'status': u'active'}
        self.assertEqual(response, expected)

    def test_should_find_inactive_user(self):
        """Tests using the search parameters to find an 'inactive' member"""
        params = {
            'url': self.url,
            'email': 'inactive@test.com',
            'cpf': self.user_invalid.member.cpf
        }

        request = self.client.get("%(url)s?cpf=%(cpf)s&email=%(email)s" % (params))
        response = json.loads(request.content)
        expected = {u'status': u'inactive'}
        self.assertEqual(response, expected)

        request = self.client.get("%(url)s?email=%(email)s" % (params))
        response = json.loads(request.content)
        expected = {u'status': u'inactive'}
        self.assertEqual(response, expected)

        request = self.client.get("%(url)s?cpf=%(cpf)s" % (params))
        response = json.loads(request.content)
        expected = {u'status': u'inactive'}
        self.assertEqual(response, expected)

    def test_should_validate_non_existant_user(self):
        """Test should validate a non existant user"""
        params = {
            'url': self.url,
            'email': 'invalid@test.com',
            'cpf': '11122233344'
        }

        request = self.client.get("%(url)s?cpf=%(cpf)s&email=%(email)s" % (params))
        response = json.loads(request.content)
        expected = {u'status': u'invalid'}
        self.assertEqual(response, expected)

        request = self.client.get("%(url)s?email=%(email)s" % (params))
        response = json.loads(request.content)
        expected = {u'status': u'invalid'}
        self.assertEqual(response, expected)

        request = self.client.get("%(url)s?cpf=%(cpf)s" % (params))
        response = json.loads(request.content)
        expected = {u'status': u'invalid'}
        self.assertEqual(response, expected)
