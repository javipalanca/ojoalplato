# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-05-12 15:12
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import ojoalplato.blog.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0025_auto_20170512_0918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(blank=True, default=ojoalplato.blog.models.get_default_user, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name='Autor'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image_header',
            field=models.ImageField(blank=True, help_text='Imagen de 850px x 398px', null=True, upload_to='/app/ojoalplato/media', verbose_name='Imagen de cabecera'),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Fecha publicación'),
        ),
    ]
