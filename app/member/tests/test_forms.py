#!/usr/bin/env python
# encoding: utf-8
from django.test import TestCase
from app.member.forms import MemberForm, UserForm
from app.member.models import Organization, City, User, Member


class FormTest(TestCase):

    def setUp(self):
        self.data = {
            'full_name': 'Valder Gallo Jr',
            'organization': 'Home',
            'address': 'Rua XXX',

            'cpf': '94463643104',
            'email': 'valdergallo@gmail.com',
            'phone': '1199492911',
            'city': 'Sao Paulo',
            'state': 'SP',
            'category': 1,
            'relationship': 'think',
            'mailing': 1,
            'contact': 1,
            'partner': 1,
            'relation_with_community': 'fake relation'
        }


class ValidUserFormTest(FormTest):

    def setUp(self):
        super(ValidUserFormTest, self).setUp()

        self.user_form = UserForm(self.data)
        self.user_form.is_valid()
        self.new_user = self.user_form.save()

    def test_form_must_be_valid(self):
        self.assertTrue(self.user_form.is_valid())

    def test_save_user(self):
        self.assertIsInstance(self.new_user, User)

    def test_should_store_first_name(self):
        self.assertEqual(self.new_user.first_name, 'Valder Gallo')

    def test_should_store_last_name(self):
        self.assertEqual(self.new_user.last_name, 'Jr')

    def test_should_store_email(self):
        self.assertEqual(self.new_user.email, self.data.get('email'))

    def test_should_store_username(self):
        self.assertEqual(self.new_user.username, self.data.get('email')[:70])


class InvalidUserFormTest(TestCase):

    def setUp(self):
        self.user_form = UserForm({})

    def test_must_be_invalid(self):
        self.assertFalse(self.user_form.is_valid())

    def test_with_no_data_should_return_email_error(self):
        self.assertTrue(self.user_form.errors.has_key('email'))

    def test_with_no_data_should_return_full_name_error(self):
        self.assertTrue(self.user_form.errors.has_key('full_name'))


class ValidMemberFormTest(FormTest):

    def setUp(self):
        super(ValidMemberFormTest, self).setUp()

        self.user_form = UserForm(self.data)
        self.user_form.is_valid()

        self.member_form = MemberForm(self.data)
        self.member_form.is_valid()
        self.user_instance = self.user_form.save()
        self.member_instance = self.member_form.save(self.user_instance)

    def test_form_must_be_valid(self):
        self.assertTrue(self.member_form.is_valid())

    def test_should_create_an_user(self):
        self.assertEqual(self.user_instance.get_full_name(), self.data.get('full_name'))
        self.assertIsInstance(self.member_instance.user, User)

    def test_should_store_a_city(self):
        city = City.objects.get(name='Sao Paulo', state='SP')
        self.assertEqual(self.member_instance.city, city)

    def test_should_store_organization(self):
        organization = Organization.objects.get(name='Home')
        self.assertEqual(self.member_instance.organization, organization)

    def test_should_store_cpf(self):
        self.assertEqual(self.member_instance.cpf, self.data.get('cpf'))

    def test_should_store_phone(self):
        self.assertEqual(self.member_instance.phone, '11-9949-2911')

    def test_should_store_address(self):
        self.assertEqual(self.member_instance.address, self.data.get('address'))

    def test_should_store_public_key(self):
        self.assertEqual(self.member_instance.public_key, self.data.get('public_key'))

    def test_should_store_category(self):
        self.assertEqual(self.member_instance.category.id, self.data.get('category'))

    def test_should_store_relation_with_community(self):
        self.assertEqual(self.member_instance.relation_with_community, self.data.get('relation_with_community'))

    def test_should_store_mailing(self):
        self.assertEqual(self.member_instance.mailing, self.data.get('mailing'))

    def test_should_store_partner(self):
        self.assertEqual(self.member_instance.partner, self.data.get('partner'))

    def test_should_change_username(self):
        self.assertEqual(self.member_instance.user.username, self.member_instance.cpf)


class InvalidUserFormTest(TestCase):

    def setUp(self):
        super(InvalidUserFormTest, self).setUp()
        self.member_form = MemberForm({})

    def test_must_be_invalid(self):
        self.assertFalse(self.member_form.is_valid())

    def test_with_no_data_should_return_category_error(self):
        self.assertTrue(self.member_form.errors.has_key('category'))

    def test_with_no_data_should_return_organization_error(self):
        self.assertTrue(self.member_form.errors.has_key('organization'))

    def test_with_no_data_should_return_state_error(self):
        self.assertTrue(self.member_form.errors.has_key('state'))

    def test_with_no_data_should_return_cpf_error(self):
        self.assertTrue(self.member_form.errors.has_key('cpf'))

    def test_with_no_data_should_return_city_error(self):
        self.assertTrue(self.member_form.errors.has_key('city'))
