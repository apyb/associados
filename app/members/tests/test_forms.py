#!/usr/bin/env python
# encoding: utf-8
from django.test import TestCase
from app.members.forms import MemberForm, UserForm
from app.members.models import Organization, City, User, Member


class FormTest(TestCase):

    def setUp(self):
        self.data = {
            'full_name': 'Valder Gallo Jr',
            'organization': 'Home',
            'address': 'Rua XXX',

            'cpf': '94463643104',
            'email': 'valdergallo@gmail.com',
            'fone': '1199492911',
            'city': 'Sao Paulo',
            'state': 'SP',
            'category': '1',
            'relationship': 'think',
            'mailing': 1,
            'contact': 1,
            'partner': 1,
            'relation_with_community':'fake relation'
        }


class UserFormTest(FormTest):

    def setUp(self):
        super(UserFormTest, self).setUp()

        self.user_form = UserForm(self.data)
        self.user_form.is_valid()
        self.new_user = self.user_form.save()

    def test_save_user(self):
        self.assertIsInstance(self.new_user, User)

    def test_should_store_first_name(self):
        self.assertEqual(self.new_user.first_name, 'Valder Gallo')

    def test_should_store_last_name(self):
        self.assertEqual(self.new_user.last_name, 'Jr')

    def test_should_store_email(self):
        self.assertEqual(self.new_user.email, self.data.get('email'))

    def test_should_store_username(self):
        self.assertEqual(self.new_user.username, 'valdergallojr')



class MemberFormTest(FormTest):

    def setUp(self):
        super(MemberFormTest, self).setUp()

        self.user_form = UserForm(self.data)
        self.user_form.is_valid()

        self.member_form = MemberForm(self.data)
        self.member_form.is_valid()
        self.user_instance = self.user_form.save()
        self.member_instance = self.member_form.save(self.user_instance)

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

    def test_should_store_fone(self):
        self.assertEqual(self.member_instance.fone, self.data.get('fone'))

    def test_should_store_address(self):
        self.assertEqual(self.member_instance.address, self.data.get('address'))

    def test_should_store_public_key(self):
        self.assertEqual(self.member_instance.public_key, self.data.get('public_key'))

    def test_should_store_category(self):
        self.assertEqual(self.member_instance.category, self.data.get('category'))

    def test_should_store_relation_with_community(self):
        self.assertEqual(self.member_instance.relation_with_community, self.data.get('relation_with_community'))

    def test_should_store_mailing(self):
        self.assertEqual(self.member_instance.mailing, self.data.get('mailing'))

    def test_should_store_partner(self):
        self.assertEqual(self.member_instance.partner, self.data.get('partner'))

#
#
#CATEGORY_CHOICE = (('1', _('Student')),
#                   ('2', _('Member')))
#
#user = models.OneToOneField(User)
#organization = models.ForeignKey(Organization, null=True, blank=True)
#cpf = models.CharField(_('CPF'), max_length=11, db_index=True)
#fone = models.CharField(_('Fone'), max_length=50, null=True, blank=True)
#address = models.TextField(_('Address'), null=True, blank=True)
#city = models.ForeignKey(City, db_index=True)
#public_key = models.FileField(_('Public Key'), upload_to=get_public_key_storage_path,
#    null=True, blank=True)
#category = models.CharField(_('Category'), max_length=1, choices=CATEGORY_CHOICE,
#    db_index=True)
#relation_with_community = models.TextField(_('Relation with community'), null=True, blank=True)
#malling = models.BooleanField(_('Malling'), default=True)
#partner = models.BooleanField(_('Partner'), default=True)
#
