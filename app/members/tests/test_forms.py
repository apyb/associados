#!/usr/bin/env python
# encoding: utf-8
from django.test import TestCase
from app.members.forms import MemberForm, UserForm
from app.members.models import Organization, User, Category, Member
from app.payment.models import Payment, PaymentType, Transaction
from app.members.tests.helpers import create_user_with_member


class UserFormTest(TestCase):
    data = {
        'first_name': 'Valder',
        'last_name': 'Gallo Jr',
        'email': 'valdergallo@gmail.com',
    }


class MemberFormTest(TestCase):
    data = {
        'first_name': 'Valder',
        'last_name': 'Gallo Jr',
        'email': 'valdergallo@gmail.com',

        'organization': 'Home',
        'address': 'Rua XXX',

        'cpf': '94463643104',
        'phone': '1199492911',
        'location': 'Sao Paulo',
        'category': '1',
        'relationship': 'think',
        'mailing': 1,
        'contact': 1,
        'partner': 1,
        'relation_with_community': 'fake relation'
    }


class ValidUserFormTest(UserFormTest):
    def setUp(self):
        self.user_form = UserForm(self.data)
        self.user_form.is_valid()
        self.new_user = self.user_form.save()

    def test_form_must_be_valid(self):
        self.assertTrue(self.user_form.is_valid())

    def test_save_user(self):
        self.assertIsInstance(self.new_user, User)

    def test_should_store_first_name(self):
        self.assertEqual(self.new_user.first_name, 'Valder')

    def test_should_store_last_name(self):
        self.assertEqual(self.new_user.last_name, 'Gallo Jr')

    def test_should_store_email(self):
        self.assertEqual(self.new_user.email, self.data.get('email'))


class InvalidUserFormTest(TestCase):
    def setUp(self):
        self.user_form = UserForm({})

    def test_must_be_invalid(self):
        self.assertFalse(self.user_form.is_valid())

    def test_with_no_data_should_return_first_name_error(self):
        self.assertIn('first_name', self.user_form.errors)

    def test_with_no_data_should_return_last_name_error(self):
        self.assertIn('last_name', self.user_form.errors)

    def test_with_no_data_should_return_email_error(self):
        self.assertIn('email', self.user_form.errors)


class ValidMemberFormTest(MemberFormTest):
    def setUp(self):
        self.user_form = UserForm(self.data)
        self.user_form.is_valid()

        self.member_form = MemberForm(self.data)
        self.member_form.is_valid()
        self.user_instance = self.user_form.save()
        self.member_instance = self.member_form.save(self.user_instance)

    def test_form_must_be_valid(self):
        self.assertTrue(self.member_form.is_valid())

    def test_should_store_location(self):
        self.assertEqual(self.member_instance.location, 'Sao Paulo')

    def test_should_store_organization(self):
        organization = Organization.objects.get(name='Home')
        self.assertEqual(self.member_instance.organization, organization)

    def test_should_store_cpf(self):
        self.assertEqual(self.member_instance.cpf, self.data.get('cpf'))

    def test_should_store_phone(self):
        self.assertEqual(self.member_instance.phone, '11-9949-2911')

    def test_should_store_address(self):
        self.assertEqual(self.member_instance.address, self.data.get('address'))

    def test_should_store_category(self):
        category = Category.objects.get(id=self.data.get('category'))
        self.assertEqual(self.member_instance.category, category)

    def test_should_store_relation_with_community(self):
        self.assertEqual(self.member_instance.relation_with_community, self.data.get('relation_with_community'))

    def test_should_store_mailing(self):
        self.assertEqual(self.member_instance.mailing, self.data.get('mailing'))

    def test_should_store_partner(self):
        self.assertEqual(self.member_instance.partner, self.data.get('partner'))


class InvalidMemberFormTest(MemberFormTest):
    def setUp(self):
        self.member_form = MemberForm({})

    def test_must_be_invalid(self):
        self.assertFalse(self.member_form.is_valid())

    def test_with_no_data_should_return_category_error(self):
        self.assertIn('category', self.member_form.errors)

    def test_with_no_data_should_return_cpf_error(self):
        self.assertIn('cpf', self.member_form.errors)


class CreateNewMember(MemberFormTest):
    def setUp(self):
        self.member_form = MemberForm(self.data)

    def test_if_form_is_valid(self):
        self.assertTrue(self.member_form.is_valid())

    def test_save_form(self):
        user = User.objects.create(username='test')
        self.member_form.is_valid()
        self.member_form.save(user)
        self.assertEqual(Member.objects.count(), 1)
