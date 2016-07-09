# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(null=True, blank=True)),
                ('code', models.CharField(max_length=50, null=True, blank=True)),
                ('valid_until', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.DecimalField(max_digits=5, decimal_places=2)),
                ('duration', models.IntegerField(default=1, help_text=b'In days')),
                ('category', models.ForeignKey(to='members.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('code', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=1, choices=[(b'1', 'Awaiting Payment'), (b'2', 'In analysis'), (b'3', 'Paid'), (b'4', 'Available'), (b'5', 'In dispute'), (b'6', 'Returned'), (b'7', 'Cancelled')])),
                ('price', models.DecimalField(max_digits=5, decimal_places=2)),
                ('payment', models.ForeignKey(to='payment.Payment')),
            ],
        ),
        migrations.AddField(
            model_name='payment',
            name='last_transaction',
            field=models.ForeignKey(related_name='last_transaction', blank=True, to='payment.Transaction', null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='member',
            field=models.ForeignKey(to='members.Member'),
        ),
        migrations.AddField(
            model_name='payment',
            name='type',
            field=models.ForeignKey(to='payment.PaymentType'),
        ),
    ]
