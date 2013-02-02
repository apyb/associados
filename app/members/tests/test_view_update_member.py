# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from app.members.models import Member, Category, City, Organization
from app.members.tests.helpers import create_user_with_member
from lxml import html as lhtml


class MemberChangeView(TestCase):
    def setUp(self):
        super(MemberChangeView, self).setUp()

        self.url = reverse('members-form')
        self.user = create_user_with_member(first_name='test', last_name='fake')
        self.client.login(username='testfake', password='pass')
        self.response = self.client.get(self.url)
        self.dom = lhtml.fromstring(self.response.content)

        self.data = {
            u'category': u'1',
            u'location': u'editou',
            u'organization': u'editou',
            u'relation_with_community': u'editou',
            u'phone': u'12-1212-1212',
            u'cpf': u'71763224490',
            u'state': u'editou',
            u'address': u'address',
            u'partner': u'',
            u'mailing': u'',
            u'email': u'john@doe.com',
            u'first_name': u'editou',
            u'last_name': u'editou',
        }

    def test_should_have_a_route(self):
        try:
            reverse('members-form')
        except NoReverseMatch:
            self.fail("Reversal of url named 'members-form' failed with NoReverseMatch")

    def test_route_must_be_protected(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, 'login/?next=/members/update/')

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


class MemberChangeWithErrorView(TestCase):
    def setUp(self):
        super(MemberChangeWithErrorView, self).setUp()

        self.url = reverse('members-form')
        self.user = create_user_with_member(first_name='test', last_name='fake')
        self.client.login(username='testfake', password='pass')
        self.response = self.client.get(self.url)
        self.dom = lhtml.fromstring(self.response.content)

        self.data = {
            u'category': u'1',
            u'partner': u'',
            u'mailing': u'',
            u'email': u'john@doe.com',
            u'first_name': u'editou',
            u'last_name': u'editou',
        }

    def test_post_with_correcly_data_should_update_a_member(self):
        response = self.client.post(self.url, self.data)

        self.assertIn('Ocorreu um erro ao tentar salvar seus dados. verifique o form abaixo.', response.content)
