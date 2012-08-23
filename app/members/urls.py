# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from app.members.views import MemberListView, member_form, dashboard, SignupView

urlpatterns = patterns('',
    url(r'^signup/$', SignupView.as_view(), name='members-signup'),
    url(r'^list/$', MemberListView.as_view(), name='members-list'),
    url(r'^change/$', member_form, name='members-form'),  # may it should be /update/
    url(r'^dashboard/$', dashboard, name='members-dashboard'),
)