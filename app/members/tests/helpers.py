#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from app.members.models import Category, Member
from model_bakery import baker


def create_user_with_member(first_name='test', last_name='test', email='test@test.com', password='pass', category=None):
    category = category or Category.objects.get(id=1)

    user = User.objects.create_user(
        username='%s%s' % (first_name, last_name),
        email=email,
        password=password
    )
    user.first_name = first_name
    user.last_name = last_name
    user.save()

    baker.make(Member, user=user, category=category, github_user=None)
    return user
