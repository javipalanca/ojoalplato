# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-06-06 19:51
from __future__ import unicode_literals

from django.db import migrations
import likert_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0014_auto_20170605_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='stars',
            field=likert_field.models.LikertField(blank=True, default=0, null=True, verbose_name='Estrellas michelín'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='suns',
            field=likert_field.models.LikertField(blank=True, default=0, null=True, verbose_name='Soles Repsol'),
        ),
    ]
