# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-03 03:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='activity',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('distance', models.FloatField(max_length=30)),
                ('moving_time', models.DurationField(max_length=30)),
                ('elapsed_time', models.DurationField(max_length=30)),
                ('total_elevation_gain', models.FloatField(max_length=30)),
                ('elev_high', models.FloatField(max_length=30)),
                ('elev_low', models.FloatField(max_length=30)),
                ('type', models.CharField(max_length=30)),
                ('start_date_local', models.DateTimeField(max_length=30)),
                ('average_speed', models.FloatField(max_length=30)),
                ('max_watts', models.IntegerField(max_length=30)),
                ('calories', models.IntegerField(max_length=30)),
                ('photos', models.URLField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='athlete',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=30)),
                ('lastname', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='activity',
            name='althlete_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.athlete'),
        ),
    ]
