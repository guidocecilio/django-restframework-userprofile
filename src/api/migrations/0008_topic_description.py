# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-21 07:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20170721_0708'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='description',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
