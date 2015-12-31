# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.management import call_command
from django.db import migrations


def load_fixture(apps, schema_editor):
    call_command('loaddata', 'payment_types.json', app_label='payment')


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_fixture)
    ]
