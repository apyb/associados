#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from app.members.models import Category, Member
from django_dynamic_fixture import G

def create_user(first_name, last_name, category=None):
    category = category or Category.objects.get(id=1)

    user = User.objects.create_user(
        username='%s%s' % (first_name, last_name),
        email='test@test.com',
        password='pass'
    )
    user.first_name=first_name
    user.last_name=last_name
    user.save()

    G(Member, user=user, category=category)
    return user