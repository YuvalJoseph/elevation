# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-25 01:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_auto_20160424_1429'),
    ]

    operations = [
        migrations.CreateModel(
            name='club',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
            ],
        ),
    ]