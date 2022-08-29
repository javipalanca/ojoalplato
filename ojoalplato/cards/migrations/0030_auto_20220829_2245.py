# Generated by Django 3.2.13 on 2022-08-29 20:45

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0029_auto_20220829_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='wine',
            name='year',
            field=models.IntegerField(blank=True, max_length=5, null=True, verbose_name='Añada'),
        ),
        migrations.AlterField(
            model_name='wine',
            name='cata_olf_aroma_3',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(0, 'Madera'), (1, 'Tabaco'), (2, 'Frutos secos'), (3, 'Cuero'), (4, 'Acético'), (5, 'Mohoso'), (6, 'Corcho')], max_length=10, null=True, verbose_name='Aroma (Carácter) Terciarios (maduración)'),
        ),
    ]
