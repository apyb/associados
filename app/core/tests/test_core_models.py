#!/usr/bin/env python
from django.test import TestCase
from app.core.models import TestDefaultFields
from model_bakery import baker


class ManagerTest(TestCase):

    def setUp(self):
        baker.make(TestDefaultFields, _quantity=4)

    def test_basic_addition_default(self):
        self.assertEqual(TestDefaultFields.objects.count(), 4)

    def test_not_show_canceled(self):
        testfield = TestDefaultFields.objects.all()[0]
        testfield.active = False
        testfield.save()

        self.assertEqual(TestDefaultFields.objects.count(), 3)
        self.assertFalse(TestDefaultFields.objects.filter(id=testfield.id))

    def test_show_canceled(self):
        testfield = TestDefaultFields.objects.all()[0]
        testfield.active = False
        testfield.save()

        self.assertEqual(TestDefaultFields.canceleds.count(), 1)
        self.assertTrue(TestDefaultFields.canceleds.filter(id=testfield.id))
