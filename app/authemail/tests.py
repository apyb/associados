# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, UserManager
from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from app.members.models import Member, Category, City, Organization
from django_dynamic_fixture import G
from app.members.tests.helpers import create_user_with_member
from app.authemail.forms import RegisterForm


class ValidFormTest(TestCase):
    def setUp(self):
        super(ValidFormTest, self).setUp()

        self.data = {
            u'email': u'fake_user@fake.com',
            u'password1': u'fake_pass',
            u'password2': u'fake_pass',
            }
        self.form = RegisterForm(data=self.data)

    def test_should_be_valid(self):
        self.assertTrue(self.form.is_valid())

    def test_should_create_a_user(self):
        self.form.is_valid()
        user = self.form.save()

        try:
            User.objects.get(email=self.data['email'])
        except Member.DoesNotExist:
            self.fail("User does not exist")#

    def test_should_persist_user_data(self):
        self.form.is_valid()
        user = self.form.save()

        self.assertEqual(user.email, u'fake_user@fake.com')
        self.assertTrue(user.check_password('fake_pass'))

    def test_should_persist_the_username_of_email(self):
        self.form.is_valid()
        user = self.form.save()
        self.assertEqual(user.username, u'fake_user')

    def test_should_add_user_id_when_username_already_exists(self):
        self.form.is_valid()
        self.form.save()

        user = self.form.save()
        expected_username = "fake_user_%s" % user.id
        self.assertEqual(user.username, expected_username)


class InValidFormTest(TestCase):
    def setUp(self):
        super(InValidFormTest, self).setUp()

        self.data = {
            u'email': u'',
            u'password1': u'',
            u'password2': u'',
            }

        self.form = RegisterForm(data=self.data)

    def test_should_be_invalid(self):
        self.assertFalse(self.form.is_valid())
