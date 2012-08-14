# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from app.members.views import MemberListView, register, member_form, dashboard

urlpatterns = patterns('',
    url(r'^register/$', register, name='member-register'),
    url(r'^list/$', MemberListView.as_view(), name='members-list'),
    url(r'^change/$', member_form, name='members-form'),  # may it should be /update/
    url(r'^dashboard/$', dashboard, name='members-form'),
)