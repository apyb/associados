#!/usr/bin/env python
# encoding: utf-8
"""
models.py

Created by Valder Gallo on 2012-01-29.
Copyright (c) 2012 valdergallo. All rights reserved.
"""
from django.db import models
from managers import CanceledManager, ActiveManager


class DefaultFields(models.Model):
    """
    Class Abstract Fields with latitude (lat), longitude (lon)
    created date (created_at), updated date (updated_at)
    and active (active)
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, db_index=True)

    objects = ActiveManager()
    canceleds = CanceledManager()

    class Meta:
        abstract = True


class DefaultGeoFields(DefaultFields):
    """
    Class Abstract Fields with created date (created_at),
    updated date (updated_at) and active
    """
    lat = models.FloatField(null=True, blank=True, db_index=True)
    lon = models.FloatField(null=True, blank=True, db_index=True)

    objects = ActiveManager()
    canceleds = CanceledManager()

    class Meta:
        abstract = True


class TestDefaultFields(DefaultGeoFields):
    "just for test manager"
    pass
