# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-08-05 14:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0016_restaurant_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-mail'),
        ),
    ]
