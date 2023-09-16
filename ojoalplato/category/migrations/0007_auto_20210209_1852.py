# Generated by Django 3.1.6 on 2021-02-09 17:52

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0006_auto_20170512_1504'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='category',
            managers=[
                ('tree', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='category',
            name='level',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='category',
            name='lft',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='category',
            name='rght',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='category',
            name='thumbnail',
            field=models.ImageField(blank=True, default='uncategorized.gif', null=True, upload_to='.'),
        ),
    ]