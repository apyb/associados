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
        user_valid = create_user_with_member(
            first_name='active'
        )
        self.member_valid = user_valid.member
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
            status='done',
            price=50.0
        )
    
        # Inactive member
        user_invalid = create_user_with_member(
            first_name='inactive',
            email='invalid@test.com'
        )

    def test_should_have_a_route(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_should_receive_error_json(self):
        request = self.client.get(self.url)
        response = json.loads(request.content)
        expected = {"error": u"nenhum parâmetro válido informado. Opções: ['name', 'email', 'cpf', 'phone', 'organization']"}

        self.assertEqual(response, expected)

    def test_should_find_active_user(self):
        """Testes usando os parametros de busca para encontrar usuario valido"""
        name = 'active'
        request = self.client.get("%s?name=%s" % (self.url, name))
        response = json.loads(request.content)
        expected = {'status':'ativo'}
        self.assertEqual(response, expected)

    def test_should_find_inactive_user(self):
        """Testes usando os parametros de busca para encontrar usuario invalido"""
        name = 'inactive'
        request = self.client.get("%s?name=%s" % (self.url, name))
        response = json.loads(request.content)
        expected = {'status':'inativo'}
        self.assertEqual(response, expected)

    def test_should_validate_non_existant_user(self):
        name = 'invalid'
        request = self.client.get("%s?name=%s" % (self.url, name))
        response = json.loads(request.content)
        expected = {'status':'invalido'}
        self.assertEqual(response, expected)