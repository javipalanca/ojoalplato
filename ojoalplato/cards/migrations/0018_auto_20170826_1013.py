# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-08-26 08:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0017_restaurant_email'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['name'], 'verbose_name': 'Receta', 'verbose_name_plural': 'Recetas'},
        ),
        migrations.AlterModelOptions(
            name='restaurant',
            options={'ordering': ['name'], 'verbose_name': 'Restaurante', 'verbose_name_plural': 'Restaurantes'},
        ),
        migrations.AlterModelOptions(
            name='wine',
            options={'ordering': ['name'], 'verbose_name': 'Vino', 'verbose_name_plural': 'Vinos'},
        ),
    ]
