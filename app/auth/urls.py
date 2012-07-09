#!/usr/bin/env python
# encoding: utf-8
from django.conf.urls import patterns, url
from app.auth.views import register

urlpatterns = patterns('',
    url(r'^$', register),
)
