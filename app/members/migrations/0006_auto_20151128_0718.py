# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_member_municipio_codigo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='municipio_codigo',
            field=models.ForeignKey(related_name='municipio_org_mun', verbose_name='Munic\xedpio', blank=True, to='municipios.Municipio', null=True),
        ),
    ]
