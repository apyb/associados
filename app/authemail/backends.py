# -*- coding: utf-8 -*-


from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class EmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        users = User.objects.filter(Q(email=username) | Q(username=username), is_active=True)
        if not users:
            return None

        try:
            if users[0].check_password(password):
                return users[0]
        except ValueError:
            return None