# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-02 05:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cwo', '0010_auto_20160801_1706'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='territoryregion',
            name='region_id',
        ),
        migrations.RemoveField(
            model_name='territoryregion',
            name='territory_id',
        ),
        migrations.AddField(
            model_name='territoryregion',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cwo.Region'),
        ),
        migrations.AddField(
            model_name='territoryregion',
            name='territory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cwo.Territory'),
        ),
    ]
