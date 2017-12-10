# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-25 11:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '__first__'),
        ('blog', '0019_auto_20160825_0802'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='recipe_card',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cards.Recipe', verbose_name='Ficha de receta'),
        ),
        migrations.AddField(
            model_name='post',
            name='restaurant_card',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cards.Restaurant', verbose_name='Ficha de restaurante'),
        ),
        migrations.AddField(
            model_name='post',
            name='wine_card',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cards.Wine', verbose_name='Ficha de vino'),
        ),
    ]
