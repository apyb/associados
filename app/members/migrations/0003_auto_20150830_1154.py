# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_auto_20150830_0626'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='diretoria',
            field=models.BooleanField(default=False, verbose_name=b'Diretoria'),
        ),
        migrations.AddField(
            model_name='member',
            name='thumb_image',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Thumbimage', blank=True),
        ),
    ]
