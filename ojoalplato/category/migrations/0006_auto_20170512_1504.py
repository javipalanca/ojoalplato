# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-05-12 15:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0005_auto_20170512_0918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='thumbnail',
            field=models.ImageField(blank=True, default='/app/ojoalplato/mediauncategorized.gif', null=True, upload_to='/app/ojoalplato/media'),
        ),
    ]
