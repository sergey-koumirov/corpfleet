# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-01 17:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cwo', '0009_participant_war'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='territory',
            name='war_id',
        ),
        migrations.AddField(
            model_name='territory',
            name='war',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cwo.War'),
        ),
    ]
