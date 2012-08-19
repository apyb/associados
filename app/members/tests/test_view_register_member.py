# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, UserManager
from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from app.members.models import Member, Category, City, Organization
from django_dynamic_fixture import G
from app.members.tests.helpers import create_user_with_member

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
            u'first_name': u'',
            u'last_name': u'',
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
            u'first_name': u'john',
            u'last_name': u'doe',
            u'address': u'Rua XXX',
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
        self.assertContains(self.response, u'This field is required.', count=4)

    def test_post_with_correcly_data_should_create_a_member(self):
        self.response = self.client.post(self.url, data=self.data)
        try:
            Member.objects.get(cpf=self.data['cpf'])
        except Member.DoesNotExist:
            self.fail("Member does not exist")

    def test_post_with_correcly_data_should_persiste_POST_data(self):
        response = self.client.post(self.url, self.data)

        member = Member.objects.get(cpf=self.data['cpf'])

        self.assertEqual(member.category, Category.objects.get(id=1))
        self.assertEqual(member.city, City.objects.get(name='Rio de Janeiro'))
        self.assertEqual(member.organization, Organization.objects.get(name='globo'))
        self.assertEqual(member.relation_with_community, u'')
        self.assertEqual(member.phone, u'21-8447-9744')
        self.assertEqual(member.cpf, u'48296130840')
        self.assertEqual(member.city.state, u'RJ')
        self.assertEqual(member.address, u'Rua XXX')
        self.assertEqual(member.partner, True)
        self.assertEqual(member.mailing, True)
        self.assertEqual(member.user.email, u'john@doe.com')
        self.assertEqual(member.user.first_name, u'john')
        self.assertEqual(member.user.last_name, u'doe')

#    def test_post_with_correcly_data_should_redirect_to_payment(self):
#        self.response = self.client.post(self.url, data=self.data)
#        member = Member.objects.get(cpf=self.data['cpf'])
#        payment_url = reverse('payment', kwargs={'member_id':member.id})
#
#        self.assertEqual(self.response.status_code, 302)
#        self.assertTrue(self.response['location'].endswith(payment_url) )
