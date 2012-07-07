# -*- coding: utf-8 -*-
from django.contrib.flatpages.models import FlatPage
from django.test import TestCase
from lxml import html as lhtml

class FlatpagesTest(TestCase):

    def setUp(self):
        super(FlatpagesTest, self).setUp()
        self.flatpage = FlatPage.objects.get(id=1)
        self.response = self.client.get(self.flatpage.get_absolute_url())

    def test_flatpage_view_works(self):
        self.assertEqual(self.response.status_code, 200)

    def test_flatpage_render_custom_template(self):
        templates = [template.name for template in self.response.templates]
        self.assertIn('flatpages/default.html', templates)

    def test_flatpage_has_base_template(self):
        templates = [template.name for template in self.response.templates]
        self.assertIn('base.html', templates)

    def test_flatpage_renders_title(self):
        dom = lhtml.fromstring(self.response.content)
        self.assertEqual(dom.cssselect('title')[0].text, self.flatpage.title)


