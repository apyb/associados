# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from unittest.case import TestCase
from app.members.tests.helpers import create_user_with_member
from app.payment.models import Payment, PaymentType, Transaction


class TransacitonModelTestCase(TestCase):
    def test_should_have_code(self):
        self.assert_field_in('code', Transaction)

    def test_should_have_status(self):
        self.assert_field_in('status', Transaction)

    def test_should_have_payment(self):
        self.assert_field_in('payment', Transaction)

        payment_field = Transaction._meta.get_field_by_name('payment')[0]
        self.assertIsInstance(payment_field, models.ForeignKey)
        self.assertEqual(Payment, payment_field.related.model)

    def test_get_checkout_url(self):
        t = Transaction(code="123")
        expected_url = settings.PAGSEGURO_WEBCHECKOUT + "123"
        self.assertEqual(expected_url, t.get_checkout_url())

    def assert_field_in(self, field_name, model):
        self.assertIn(field_name, model._meta.get_all_field_names())


class TransactionTestCase(TestCase):

    def test_should_upgrade_last_payment(self):
        user = create_user_with_member()
        payment = Payment.objects.create(
            member = user.member,
            type = PaymentType.objects.get(id=1)
        )
        transaction = Transaction.objects.create(
            payment=payment,
            status=0,
            code='fakecode',
            price='0.0'
        )
        self.assertEqual(transaction, payment.last_transaction)

