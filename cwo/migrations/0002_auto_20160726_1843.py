# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-26 18:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cwo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StructureType',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
        )
    ]