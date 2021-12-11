from django.urls import reverse
from django.test import TestCase
from app.members.tests.helpers import create_user_with_member


class DashboardView(TestCase):

    def setUp(self):
        self.url = reverse('members:dashboard')
        self.user = create_user_with_member(first_name='test', last_name='fake')
        self.client.force_login(self.user)
        self.response = self.client.get(self.url)

    def test_should_have_a_route(self):
        self.assertEqual(self.response.status_code, 200)

    def test_should_render_the_correctly_template(self):
        self.assertTemplateUsed(self.response, 'members/dashboard.html')

    def test_route_must_be_protected(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, '/login/?next=/members/dashboard/')

    def test_should_redirect_if_user_has_no_member_instance(self):
        self.user.member.delete()
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('members:form'))
