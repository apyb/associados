# -*- coding: utf-8 -*-
from datetime import timedelta
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db import models
from django.test import TestCase
from django.utils import timezone

from django_dynamic_fixture import G
from app.members.models import Member, Category
from app.payment.models import Payment, Transaction, PaymentType


class MemberTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="Wolverine", first_name='Logan')
        self.member = G(
            Member,
            user=self.user,
            category=Category.objects.get(id=1)
        )


class PaymentTypeTestCase(TestCase):
    def test_should_output_payment_type_information(self):
        self.payment_type = PaymentType.objects.create(
            category = Category.objects.get(id=1),
            price = 34.34,
            duration = 20
        )
        self.assertEqual(str(self.payment_type), 'Efetivo - 34.34 for 20 days')


class PaymentModelTestCase(MemberTestCase):

    def test_name_url(self):
        try:
            reverse(
                'payment',
                kwargs={
                    'member_id': self.member.id
                }
            )
        except NoReverseMatch:
            self.fail("Reversal of url named 'payment' failed with NoReverseMatch")

    def test_should_output_member_information(self):
        self.payment = Payment.objects.create(
            member=self.member,
            type=PaymentType.objects.get(id=1),
            date=timezone.now(),
            valid_until=timezone.now() + timedelta(days=10, minutes=1)
        )
        self.assertEqual(str(self.payment), 'payment from Logan')

    def test_should_have_member(self):
        self.assert_field_in('member', Payment)

    def test_member_should_be_a_foreign_key(self):
        member_field = Payment._meta.get_field('member')
        self.assertIsInstance(member_field, models.ForeignKey)
        self.assertEqual(Member, member_field.related_model)

    def test_should_have_date(self):
        self.assert_field_in('date', Payment)

    def test_date_should_be_datetime_field(self):
        date_field = Payment._meta.get_field('date')
        self.assertIsInstance(date_field, models.DateTimeField)

    def test_should_have_valid_until(self):
        self.assert_field_in('valid_until', Payment)

    def test_valid_until_should_be_date_field(self):
        date_field = Payment._meta.get_field('valid_until')
        self.assertIsInstance(date_field, models.DateField)

    def test_should_have_type(self):
        self.assert_field_in('type', Payment)

    def test_type_should_be_a_foreign_key(self):
        type_field = Payment._meta.get_field('type')
        self.assertIsInstance(type_field, models.ForeignKey)
        self.assertEqual(PaymentType, type_field.related_model)

    def test_payment_done_should_be_false_if_has_not_a_transaction(self):
        self.assertFalse(Payment().done())

    def test_payment_done_should_be_false_if_transactions_isnt_done(self):
        type = PaymentType.objects.get(id=1)
        payment = Payment.objects.create(
            member=self.member,
            type=type
        )
        Transaction.objects.create(
            payment=payment,
            status=1,
            code="xpto",
            price="897.02"
        )
        self.assertFalse(payment.done())

    def test_payment_done_should_be_truth_if_transactions_is_done(self):
        type = PaymentType.objects.get(id=1)
        payment = Payment.objects.create(
            member=self.member,
            type=type
        )
        Transaction.objects.create(
            payment=payment,
            status=3,
            code="xpto",
            price="543.21"
        )
        self.assertTrue(payment.done())

    def assert_field_in(self, field_name, model):
        self.assertIn(field_name, [f.name for f in model._meta.get_fields()])


