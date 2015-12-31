# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_auto_20150830_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='diretoria',
            field=models.NullBooleanField(default=False, verbose_name=b'Diretoria'),
        ),
    ]
