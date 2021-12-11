#!/usr/bin/env python
from django.db import models
from .managers import CanceledManager, ActiveManager


class DefaultFields(models.Model):
    """
    Class Abstract created date (created_at), updated date (updated_at)
    and active (active)
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, db_index=True)

    objects = ActiveManager()
    canceleds = CanceledManager()

    class Meta:
        abstract = True


class TestDefaultFields(DefaultFields):
    "just for test manager"
    pass
