# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, UserManager
from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from app.members.models import Member, Category
from django_dynamic_fixture import G
from app.members.tests.helpers import create_user

class MemberListViewTest(TestCase):

    def setUp(self):
        super(MemberListViewTest, self).setUp()

        category = Category.objects.get(id=2)
        create_user(first_name='test', last_name='test')
        create_user(first_name='dolor', last_name='sit')
        create_user(first_name='lorem', last_name='ipsum', category=category)
        create_user(first_name='amet', last_name='consectetur', category=category)

        self.url = reverse('members-list')
        self.response = self.client.get(self.url)


    def test_should_have_a_route(self):
        self.assertEqual(self.response.status_code, 200)

    def test_should_render_the_correctly_template(self):
        self.assertTemplateUsed(self.response, 'members/member_list.html')

    def test_should_render_the_members(self):
        self.assertIn('test test', self.response.rendered_content)
        self.assertIn('Student', self.response.rendered_content)

    def test_should_search_members(self):
        response = self.client.get(self.url, {
            'q': 'te',
        })
        self.assertIn('test test', response.rendered_content)
        self.assertIn('amet consectetur', response.rendered_content)
        self.assertNotIn('dolor sit', response.rendered_content)
        self.assertNotIn('lorem ipsum', response.rendered_content)

    def test_should_filter_members(self):
        response = self.client.get(self.url, {
            'category': 1,
        })
        self.assertIn('test test', response.rendered_content)
        self.assertIn('dolor sit', response.rendered_content)
        self.assertNotIn('lorem ipsum', response.rendered_content)
        self.assertNotIn('amet consectetur', response.rendered_content)

    def test_should_search_and_filter_members(self):
        response = self.client.get(self.url, {
            'q': 'te',
            'category': 1,
        })
        self.assertIn('test test', response.rendered_content)
        self.assertIn('dolor sit', response.rendered_content)
        self.assertNotIn('lorem ipsum', response.rendered_content)
        self.assertNotIn('amet consectetur', response.rendered_content)

class MemberRegisterView(TestCase):
    def setUp(self):
        super(MemberRegisterView, self).setUp()

        self.url = reverse('member-register')

        self.empty_data = {
            u'category': u'',
            u'city': u'',
            u'organization': u'',
            u'fone': u'',
            u'cpf': u'',
            u'phone': u'',
            u'state': u'AC',
            u'relation_with_community': u'',
            u'full_name': u'',
            u'address': u'',
            u'partner': u'on',
            u'mailing': u'on',
            u'email': u''
        }

        self.data = {
            u'category': u'1',
            u'city': u'Rio de Janeiro',
            u'organization': u'globo',
            u'relation_with_community': u'',
            u'phone': u'2184479744',
            u'state': u'RJ',
            u'cpf': u'48296130840',
            u'full_name': u'john doe',
            u'address': u'',
            u'partner': u'on',
            u'mailing': u'on',
            u'email': u'john@doe.com'
        }


    def test_should_have_a_route(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_should_render_the_correctly_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'members/member_register.html')

    def test_post_with_blank_fields_should_return_error(self):
        self.response = self.client.post(self.url, data=self.empty_data)
        self.assertContains(self.response, u'Este campo é obrigatório.', count=6)

    def test_post_with_correcly_data_should_created_a_member(self):
        self.response = self.client.post(self.url, data=self.data)
        try:
            Member.objects.get(cpf=self.data['cpf'])
        except Member.DoesNotExist:
            self.fail("Member does not exist")

    def test_post_with_correcly_data_should_redirect_to_payment(self):
        self.response = self.client.post(self.url, data=self.data)
        member = Member.objects.get(cpf=self.data['cpf'])
        payment_url = reverse('payment', kwargs={'member_id':member.id})

        self.assertEqual(self.response.status_code, 302)
        self.assertTrue(self.response['location'].endswith(payment_url) )


class MemberChangeView(TestCase):
    def setUp(self):
        super(MemberChangeView, self).setUp()


        self.url = reverse('members-form')
        user = create_user(first_name='test', last_name='fake')
        self.client.login(username='testfake', password='pass')
        self.response = self.client.get(self.url)

    def test_should_have_a_route(self):
        try:
            reverse('members-form')
        except NoReverseMatch:
            self.fail("Reversal of url named 'members-form' failed with NoReverseMatch")

    def test_route_must_be_protected(self):
        self.client.logout()
        self.response = self.client.get(self.url)
        self.assertRedirects(self.response, 'login/?next=/members/change/')

    def test_should_responds_correcly(self):
        self.assertEqual(self.response.status_code, 200)
#
#    def test_should_render_the_correctly_template(self):
#        self.assertTemplateUsed(self.response, 'members/member_list.html')
