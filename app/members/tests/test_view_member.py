# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, UserManager
from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from app.members.models import Member, Category, City, Organization
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
        self.assertContains(self.response, u'This field is required.', count=6)

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
        self.user = create_user(first_name='test', last_name='fake')
        self.client.login(username='testfake', password='pass')
        self.response = self.client.get(self.url)

        self.data = {
            u'category': u'1',
            u'city': u'editou',
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
        self.response = self.client.get(self.url)
        self.assertRedirects(self.response, 'login/?next=/members/change/')

    def test_should_responds_correcly(self):
        self.assertEqual(self.response.status_code, 200)

    def test_should_render_the_correctly_template(self):
        self.assertTemplateUsed(self.response, 'members/member_form.html')

    def test_post_with_correcly_data_should_edit_a_member(self):
        response = self.client.post(self.url, self.data)

        member = Member.objects.get(user_id=self.user.id)

        self.assertEqual(member.category, Category.objects.get(id=1))
        self.assertEqual(member.city, City.objects.get(name='editou'))
        self.assertEqual(member.organization, Organization.objects.get(name='editou'))
        self.assertEqual(member.relation_with_community, u'editou')
        self.assertEqual(member.phone, u'12-1212-1212')
        self.assertEqual(member.cpf, u'71763224490')
        self.assertEqual(member.city.state, u'editou')
        self.assertEqual(member.address, u'address')
        self.assertEqual(member.partner, False)
        self.assertEqual(member.mailing, False)
        self.assertEqual(member.user.email, u'john@doe.com')
        self.assertEqual(member.user.first_name, u'editou')
        self.assertEqual(member.user.last_name, u'editou')




