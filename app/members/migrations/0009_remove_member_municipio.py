# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_auto_20151129_1312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='municipio',
        ),
    ]
