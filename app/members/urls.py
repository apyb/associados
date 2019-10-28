# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from app.members.views import MemberListView, member_form, dashboard,update_category, SignupView, member_status, member_json

urlpatterns = patterns(
    '',
    url(r'^signup/$', SignupView.as_view(), name='members-signup'),
    url(r'^list/$', MemberListView.as_view(), name='members-list'),
    url(r'^update/$', member_form, name='members-form'),
    url(r'^update-category/$', update_category, name='update-category'),
    url(r'^dashboard/$', dashboard, name='members-dashboard'),
    url(r'^status/$', member_status, name='members-status'),
    url(r'^json-list/$', member_json, name='member-json'),
)
