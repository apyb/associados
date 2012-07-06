#!/usr/bin/env python
# encoding: utf-8
"""
tests.py

Created by Valder Gallo on 2012-01-29.
Copyright (c) 2012 valdergallo. All rights reserved.
"""

from django.test import TestCase
from models import TestDefaultFields
from django_dynamic_fixture import G


class ManagerTest(TestCase):

    def setUp(self):
        G(TestDefaultFields, n=4)

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
