# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-27 15:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0007_auto_20160825_2323'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='avg_price',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Precio medio'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='menu_price',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Precio de menú'),
        ),
    ]
