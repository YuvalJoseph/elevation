# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-08 07:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_athlete_access_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='data_update',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_stamp', models.DateTimeField()),
            ],
        ),
    ]
