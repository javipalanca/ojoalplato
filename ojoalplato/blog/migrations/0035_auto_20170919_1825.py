# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-09-19 16:25
from __future__ import unicode_literals

import autoslug.fields
from django.db import migrations
import ojoalplato.blog.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0034_auto_20170919_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, max_length=200, populate_from='title', slugify=ojoalplato.blog.models.unique_slug, unique=True, verbose_name='Slug'),
        ),
    ]
