# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-03 23:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_auto_20160402_2019'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity',
            old_name='althlete_id',
            new_name='athlete_id',
        ),
        migrations.AlterField(
            model_name='activity',
            name='calories',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='photos',
            field=models.URLField(blank=True, null=True),
        ),
    ]
