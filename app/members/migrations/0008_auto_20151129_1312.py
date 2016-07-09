# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os.path
from django.db import migrations
from django.core.management import call_command

fixture_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../fixtures'))
fixture_filename = 'municipios.json'


def load_fixture(apps, schema_editor):
    fixture_file = os.path.join(fixture_dir, fixture_filename)
    call_command('loaddata', fixture_file)


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0007_auto_20151128_0823'),
    ]

    operations = [
        migrations.RunPython(load_fixture)
    ]
