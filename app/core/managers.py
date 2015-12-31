#!/usr/bin/env python
# encoding: utf-8
from django.db import models


class ActiveManager(models.Manager):
    def get_queryset(self):
        "Active by default"
        return super(ActiveManager, self).get_queryset().filter(active=True)


class CanceledManager(models.Manager):
    def get_queryset(self):
        "Show canceled content"
        return super(CanceledManager, self).get_queryset().filter(active=False)
