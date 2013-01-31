# -*- coding: utf-8 -*-
import django.contrib.auth.create_superuser
from django.contrib.auth.management import create_superuser
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
        self.assertEqual(user, User.objects.get(email=self.data['email']))

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

    def test_should_be_invalid(self):
        data = {
            u'email': u'',
            u'password1': u'',
            u'password2': u'',
        }

        self.form = RegisterForm(data=data)
        self.assertFalse(self.form.is_valid())
        self.assertEqual(self.form.errors['email'][0], 'This field is required.')
        self.assertEqual(self.form.errors['password1'][0], 'This field is required.')
        self.assertEqual(self.form.errors['password2'][0], 'This field is required.')

    def test_should_fail_if_password_mismatch(self):
        data = {
            u'email': u'fake_email@fake.com',
            u'password1': u'pass1',
            u'password2': u'pass2',
            }

        self.form = RegisterForm(data=data)
        self.assertFalse(self.form.is_valid())
        self.assertEqual(self.form.errors['password2'][0], "The two password fields didn't match.")

    def test_should_fail_if_has_another_user_with_same_email(self):
        User.objects.create(username='fake', email='fake@email.com')
        data = {
            u'email': u'fake@email.com',
            u'password1': u'pass',
            u'password2': u'pass',
            }

        self.form = RegisterForm(data=data)
        self.assertFalse(self.form.is_valid())
        self.assertEqual(self.form.errors['email'][0], "This email address already exists. Did you forget your password?")
