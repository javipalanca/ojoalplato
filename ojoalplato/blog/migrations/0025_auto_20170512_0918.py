# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-05-12 09:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0024_auto_20170430_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='comment_status',
            field=models.CharField(blank=True, choices=[('closed', 'closed'), ('open', 'open')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='guid',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='post',
            name='image_header',
            field=models.ImageField(blank=True, help_text='Imagen de 850px x 398px', null=True, upload_to='/media', verbose_name='Imagen de cabecera'),
        ),
    ]
