# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-22 19:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_post_image_header'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image_header',
            field=models.ImageField(blank=True, null=True, upload_to='/Users/jpalanca/devel/ojoalplato/ojoalplato/media', verbose_name='Imagen de cabecera'),
        ),
    ]
