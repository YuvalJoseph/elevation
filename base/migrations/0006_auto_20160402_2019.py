# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-03 03:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20160402_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='photos',
            field=models.URLField(null=True),
        ),
    ]