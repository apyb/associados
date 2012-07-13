# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib import admin as django_admin
from app.member.models import Member, Organization, City

class AdminMemberTest(TestCase):

    def test_Member_model_should_be_registered_within_the_admin(self):
        self.assertIn(Member, django_admin.site._registry)

    def test_Organization_model_should_be_registered_within_the_admin(self):
        self.assertIn(Organization, django_admin.site._registry)

    def test_Organization_model_should_be_registered_within_the_admin(self):
        self.assertIn(City, django_admin.site._registry)
