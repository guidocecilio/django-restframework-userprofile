# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-21 07:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20170721_0658'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='owner',
            new_name='user',
        ),
    ]