# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_auto_20150830_1236'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='municipio_codigo',
            field=models.IntegerField(null=True, verbose_name=b'MunicipioCodigo', blank=True),
        ),
    ]
