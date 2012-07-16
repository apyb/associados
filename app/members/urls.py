# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from app.members.views import MemberListView, register


urlpatterns = patterns('',
    url(r'^register/$', register, name='member-register'),
    url(r'^list/$', MemberListView.as_view(), name='members-list'),
)

