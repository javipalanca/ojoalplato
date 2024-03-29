# Generated by Django 3.2.13 on 2023-01-21 12:11

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0038_alter_wine_cata_gust_sensacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wine',
            name='cata_color_blanco',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(0, 'Pálido'), (1, 'Verdoso'), (2, 'Limón'), (3, 'Pajizo'), (4, 'Oro'), (5, 'Dorado'), (6, 'Ámbar'), (7, 'Amarillo')], max_length=20, null=True, verbose_name='Tonalidades del Color (Blanco)'),
        ),
    ]
