# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-21 22:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20160821_2257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_type',
            field=models.CharField(choices=[('attachment', 'attachment'), ('page', 'page'), ('post', 'post'), ('revision', 'revision')], default='draft', max_length=20),
        ),
    ]
