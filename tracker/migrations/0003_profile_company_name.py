# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-23 15:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_remove_profile_telephone_country_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='company_name',
            field=models.CharField(default='', max_length=1000, null=True),
        ),
    ]
