# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-10 21:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_data_update'),
    ]

    operations = [
        migrations.CreateModel(
            name='calendar_total',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField()),
                ('daily_elevation', models.FloatField()),
                ('cumulative_elevation', models.FloatField()),
                ('athlete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.athlete')),
            ],
        ),
        migrations.AddField(
            model_name='activity',
            name='cumulative_elevation',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
