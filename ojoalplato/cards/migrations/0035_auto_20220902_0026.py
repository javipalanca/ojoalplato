# Generated by Django 3.2.13 on 2022-09-01 22:26

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0034_alter_wine_cata_gust_valoracion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wine',
            name='cata_gust_sensacion',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(0, 'Acidez agradable'), (1, 'Acidez marcada'), (2, 'Amargor varietal suave'), (3, 'Amargor varietal marcado'), (4, 'Dulzor ligero'), (5, 'Dulzor marcado'), (6, 'Salinidad del terreno'), (7, 'Astringencia suave'), (8, 'Astringencia marcada'), (9, 'Validez alcohólica notable'), (10, 'Acuoso')], max_length=40, null=True, verbose_name='Sensacion'),
        ),
        migrations.AlterField(
            model_name='wine',
            name='cata_ribete',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(0, 'Transparente'), (1, 'Amarillo'), (2, 'Rosa'), (3, 'Violáceo'), (4, 'Azul'), (5, 'Rojo'), (6, 'Granate'), (7, 'Teja'), (8, 'Verde'), (9, 'Dorado')], max_length=20, null=True, verbose_name='Ribete'),
        ),
    ]
