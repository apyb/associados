from django.test import TestCase
from django.contrib import admin as django_admin
from app.members.models import Member, Organization, City


class AdminMemberTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/')

    def test_member_model_should_be_registered_within_the_admin(self):
        self.assertIn(Member, django_admin.site._registry)

    def test_organization_model_should_be_registered_within_the_admin(self):
        self.assertIn(Organization, django_admin.site._registry)

    def test_city_model_should_be_registered_within_the_admin(self):
        self.assertIn(City, django_admin.site._registry)
