# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from app.members.views import MemberListView, register

urlpatterns = patterns('',
    url(r'^register/$', register, name='people-member-register'),
    url(r'^list/$', MemberListView.as_view(), name='people-members-list'),
)

