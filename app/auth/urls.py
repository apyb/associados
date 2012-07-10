#!/usr/bin/env python
# encoding: utf-8
from django.conf.urls import patterns, url
from app.auth.views import register, UserListView

urlpatterns = patterns('',
    url(r'^register/$', register, name='member-register'),
    url(r'^list/$', UserListView.as_view(), name='people-members-list'),
)
