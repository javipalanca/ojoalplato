# Generated by Django 3.2.13 on 2022-08-28 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0038_auto_20210209_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=200, verbose_name='Slug'),
        ),
    ]
