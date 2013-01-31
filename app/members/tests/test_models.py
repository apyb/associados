#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.test import TestCase
from app.members.models import Category, Organization, City

class OutputInformatio(TestCase):
    def test_should_output_category_information(self):
        category = Category.objects.get(id=1)
        self.assertEqual(unicode(category), 'Efetivo')

    def test_should_output_organization_information(self):
        organization = Organization.objects.create(
            name = 'fake organization'
        )
        self.assertEqual(unicode(organization), 'fake organization')

    def test_should_output_city_information(self):
        city = City.objects.create(
            name = 'Rio de Janeiro',
            state = 'RJ'
        )
        self.assertEqual(unicode(city), 'Rio de Janeiro - RJ')
