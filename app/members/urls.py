# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from app.members.views import MemberListView, member_form, dashboard, SignupView

urlpatterns = patterns(
    '',
    url(r'^signup/$', SignupView.as_view(), name='members-signup'),
    url(r'^list/$', MemberListView.as_view(), name='members-list'),
    url(r'^update/$', member_form, name='members-form'),
    url(r'^dashboard/$', dashboard, name='members-dashboard'),
)
