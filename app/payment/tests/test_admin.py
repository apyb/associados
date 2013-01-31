# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib import admin as django_admin
from app.payment.models import PaymentType


class PaymentAdminTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/')

    def test_PaymentType_model_should_be_registered_within_the_admin(self):
        self.assertIn(PaymentType, django_admin.site._registry)
