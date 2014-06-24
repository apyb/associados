# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    'app.api.views',
    url(r'^verify-membership/$', 'verify_membership', name='verify-membership'),
)
