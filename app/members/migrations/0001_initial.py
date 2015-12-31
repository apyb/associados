# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True, db_index=True)),
                ('state', models.CharField(max_length=2, verbose_name='State', choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amap\xe1'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Cear\xe1'), ('DF', 'Distrito Federal'), ('ES', 'Esp\xedrito Santo'), ('GO', 'Goi\xe1s'), ('MA', 'Maranh\xe3o'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Par\xe1'), ('PB', 'Para\xedba'), ('PR', 'Paran\xe1'), ('PE', 'Pernambuco'), ('PI', 'Piau\xed'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rond\xf4nia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'S\xe3o Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')])),
                ('name', models.CharField(max_length=250, verbose_name='Name')),
            ],
            options={
                'ordering': ('state', 'name'),
                'verbose_name_plural': 'Cities',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('github_user', models.CharField(max_length=50, null=True, verbose_name='Github User', blank=True)),
                ('cpf', models.CharField(unique=True, max_length=11, verbose_name='CPF', db_index=True)),
                ('phone', models.CharField(max_length=50, null=True, verbose_name='Phone', blank=True)),
                ('address', models.TextField(null=True, verbose_name='Address', blank=True)),
                ('location', models.CharField(max_length=100, null=True, verbose_name='Location', blank=True)),
                ('relation_with_community', models.TextField(null=True, verbose_name='Relation with community', blank=True)),
                ('mailing', models.BooleanField(default=True, verbose_name='Mailing')),
                ('partner', models.BooleanField(default=True, verbose_name='Partner')),
                ('category', models.ForeignKey(verbose_name='Category', to='members.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True, db_index=True)),
                ('name', models.CharField(max_length=250, verbose_name='Name')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'Organizations',
            },
        ),
        migrations.AddField(
            model_name='member',
            name='organization',
            field=models.ForeignKey(blank=True, to='members.Organization', null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
