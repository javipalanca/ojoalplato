# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-27 21:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0008_auto_20160827_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='is_closed',
            field=models.BooleanField(default=False, verbose_name='Restaurante cerrado'),
        ),
    ]
