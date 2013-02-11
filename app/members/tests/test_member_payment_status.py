#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from app.members.tests.helpers import create_user_with_member
from app.payment.models import Payment, PaymentType, Transaction


class UserFormTest(TestCase):

    def setUp(self):
        super(UserFormTest, self).setUp()

        user = create_user_with_member(
            first_name='tes'
        )
        self.member = user.member
        payment_type = PaymentType.objects.create(
            category=self.member.category,
            price=50.0,
            duration=10
        )
        self.payment = Payment.objects.create(
            member=self.member,
            type=payment_type,
            date=timezone.now(),
            valid_until=timezone.now() + timedelta(days=10, minutes=1)
        )
        self.transaction = Transaction.objects.create(
            payment=self.payment,
            code='fake-code',
            status='other',
            price=50.0
        )

    def test_should_return_none_if_hasnt_a_valid_payment(self):
        self.assertEqual(self.member.get_last_payment(), None)

    def test_should_return_last_payment(self):
        self.transaction = Transaction.objects.create(
            payment=self.payment,
            code='fake-code',
            status='done',
            price=50.0
        )
        self.assertEqual(self.member.get_last_payment(), self.payment)

    def test_should_return_0_if_user_has_not_paid(self):
        self.assertEqual(self.member.get_days_to_next_payment(self.payment), 0)


    def test_should_calculate_days(self):
        self.transaction = Transaction.objects.create(
            payment=self.payment,
            code='fake-code',
            status='done',
            price=50.0
        )
        self.assertEqual(self.member.get_days_to_next_payment(self.payment), 10)
