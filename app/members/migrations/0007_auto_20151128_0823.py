# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0006_auto_20151128_0718'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='municipio_codigo',
            new_name='municipio',
        ),
    ]
