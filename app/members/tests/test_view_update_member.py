# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.utils.translation import ugettext as _
from app.members.models import Member, Category, Organization
from app.members.tests.helpers import create_user_with_member
from lxml import html as lhtml


class MemberChangeView(TestCase):

    def setUp(self):
        self.url = reverse('members-form')
        self.user = create_user_with_member(first_name='test', last_name='fake')
        self.client.login(username='testfake', password='pass')
        self.response = self.client.get(self.url)
        self.dom = lhtml.fromstring(self.response.content)

        self.data = {
            'category': '1',
            'location': 'editou',
            'organization': 'editou',
            'relation_with_community': 'editou',
            'phone': '12-1212-1212',
            'cpf': '71763224490',
            'state': 'editou',
            'address': 'address',
            'partner': '',
            'mailing': '',
            'email': 'john@doe.com',
            'first_name': 'editou',
            'last_name': 'editou',
        }

    def test_should_have_a_route(self):
        try:
            reverse('members-form')
        except NoReverseMatch:
            self.fail("Reversal of url named 'members-form' failed with NoReverseMatch")

    def test_route_must_be_protected(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, '/login/?next=/members/update/')

    def test_should_responds_correcly(self):
        self.assertEqual(self.response.status_code, 200)

    def test_should_render_the_correctly_template(self):
        self.assertTemplateUsed(self.response, 'members/member_form.html')

    def test_first_name_must_be_filled(self):
        first_name = self.dom.cssselect('input[name=first_name]')[0]
        self.assertEqual(first_name.value, self.user.first_name)

    def test_last_name_must_be_filled(self):
        last_name = self.dom.cssselect('input[name=last_name]')[0]
        self.assertEqual(last_name.value, self.user.last_name)

    def test_should_render_organization_name(self):
        organization = Organization.objects.create(
            name='organization fake'
        )
        self.user.member.organization = organization
        self.user.member.save()

        response = self.client.get(self.url)
        dom = lhtml.fromstring(response.content)
        organization_dom = dom.cssselect('#id_organization')[0]
        self.assertEqual(organization_dom.value, organization.name)

    def test_post_with_correcly_data_should_update_a_member(self):
        response = self.client.post(self.url, self.data)

        member = Member.objects.get(user_id=self.user.id)

        self.assertEqual(member.category, Category.objects.get(id=1))
        self.assertEqual(member.location, 'editou')
        self.assertEqual(member.organization, Organization.objects.get(name='editou'))
        self.assertEqual(member.relation_with_community, u'editou')
        self.assertEqual(member.phone, u'12-1212-1212')
        self.assertEqual(member.cpf, u'71763224490')
        self.assertEqual(member.address, u'address')
        self.assertEqual(member.partner, False)
        self.assertEqual(member.mailing, False)
        self.assertEqual(member.user.email, u'john@doe.com')
        self.assertEqual(member.user.first_name, u'editou')
        self.assertEqual(member.user.last_name, u'editou')

    def test_post_with_nine_digits_phone_should_update_a_member(self):
        phone_nine_digits = u'11-98765-4321'
        self.data.update(phone=phone_nine_digits)

        response = self.client.post(self.url, self.data)
        member = Member.objects.get(user_id=self.user.id)

        self.assertEqual(member.phone, phone_nine_digits)


class MemberChangeWithErrorView(TestCase):

    def setUp(self):
        self.url = reverse('members-form')
        self.user = create_user_with_member(first_name='test',
                                            last_name='fake')
        self.client.login(username='testfake', password='pass')
        self.response = self.client.get(self.url)
        self.dom = lhtml.fromstring(self.response.content)

        self.data = {
            'category': '1',
            'partner': '',
            'mailing': '',
            'first_name': 'editou',
            'last_name': 'editou',
        }

    def test_post_with_correcly_data_should_update_a_member(self):
        response = self.client.post(self.url, self.data)
        self.assertContains(response, 'Este campo é obrigatório')
