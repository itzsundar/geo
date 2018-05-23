# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-23 15:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_profile_company_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='company_website',
        ),
        migrations.AddField(
            model_name='profile',
            name='company_website',
            field=models.CharField(default='', max_length=1000, null=True),
        ),
    ]
