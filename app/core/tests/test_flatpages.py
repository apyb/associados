# -*- coding: utf-8 -*-
from django.contrib.flatpages.models import FlatPage
from django.core.urlresolvers import reverse
from django.test import TestCase
from lxml import html as lhtml

class FlatpagesTest(TestCase):

    def setUp(self):
        super(FlatpagesTest, self).setUp()
        self.flatpage = FlatPage.objects.get(id=1)
        self.response = self.client.get(self.flatpage.get_absolute_url())

    def test_should_have_a_route(self):
        self.assertEqual(self.response.status_code, 200)

    def test_should_render_the_correctly_template(self):
        templates = [template.name for template in self.response.templates]
        self.assertIn('flatpages/default.html', templates)

    def test_should_iherit_of_base_template(self):
        templates = [template.name for template in self.response.templates]
        self.assertIn('base.html', templates)

    def test_should_render_the_title(self):
        dom = lhtml.fromstring(self.response.content)
        self.assertEqual(dom.cssselect('title')[0].text, self.flatpage.title)

    def test_should_have_the_member_form_route(self):
        url = reverse('members-signup')
        self.assertContains(self.response, url)

    def test_should_have_the_member_list_route(self):
        url = reverse('members-list')
        self.assertContains(self.response, url)
