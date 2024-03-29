from django.contrib.auth.models import User, UserManager
from django.urls import reverse, NoReverseMatch
from django.test import TestCase
from app.members.models import Member, Category, City, Organization
from django.utils.translation import ugettext_lazy as _


class UserRegisterView(TestCase):
    def setUp(self):
        super(UserRegisterView, self).setUp()

        self.url = reverse('members:signup')

        self.empty_data = {
            'email': '',
            'password1': '',
            'password2': '',
        }

        self.user_data = {
            'email': 'member@mail.com',
            'password1': 'password1',
            'password2': 'password1',
        }

    def test_should_have_a_route(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_should_render_the_correctly_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'members/member_signup.html')

    def test_post_with_blank_fields_should_return_error(self):
        response = self.client.post(self.url, {'email': '', 'password1': '', 'password2': ''})
        self.assertFormError(response, 'form', 'email', _('This field is required.'))
        self.assertFormError(response, 'form', 'password1', _('This field is required.'))
        self.assertFormError(response, 'form', 'password2', _('This field is required.'))

    def test_post_with_correcly_data_should_create_a_user(self):
        self.response = self.client.post(self.url, data=self.user_data)
        self.assertEqual(User.objects.filter(email=self.user_data['email']).count(), 1)

    def test_post_with_correcly_data_should_redirect_to_members_form(self):
        self.response = self.client.post(self.url, data=self.user_data)
        members_form_url = reverse('members:form')
        self.assertRedirects(self.response, members_form_url)
