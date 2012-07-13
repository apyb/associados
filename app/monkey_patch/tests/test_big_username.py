# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.test import TestCase
from django_dynamic_fixture import G


class BigUsernameTest(TestCase):

    def test_username_size(self):
        user_field = User._meta.get_field('username')
        self.assertEqual(user_field.max_length, 255)

    def test_register_big_username(self):
        username = ''.zfill(255)
        user = G(User, username=username)
        self.assertEqual(len(user.username), 255)
