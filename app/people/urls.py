# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from app.people.views import MemberListView

urlpatterns = patterns('people.views',
    url(r'^$', MemberListView.as_view(), name='people-members-list'),
)


