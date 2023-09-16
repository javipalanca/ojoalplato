# Generated by Django 3.2.13 on 2022-08-31 17:05

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0032_auto_20220830_1616'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wine',
            name='cata_gust_acidez',
        ),
        migrations.RemoveField(
            model_name='wine',
            name='cata_gust_alcohol',
        ),
        migrations.RemoveField(
            model_name='wine',
            name='cata_gust_boca',
        ),
        migrations.RemoveField(
            model_name='wine',
            name='cata_gust_cuerpo',
        ),
        migrations.RemoveField(
            model_name='wine',
            name='cata_gust_dulzor',
        ),
        migrations.RemoveField(
            model_name='wine',
            name='cata_gust_tanino',
        ),
        migrations.RemoveField(
            model_name='wine',
            name='cata_intensidad',
        ),
        migrations.RemoveField(
            model_name='wine',
            name='cata_limpidez',
        ),
        migrations.RemoveField(
            model_name='wine',
            name='cata_olf_1a',
        ),
        migrations.RemoveField(
            model_name='wine',
            name='cata_olf_aroma_1',
        ),
        migrations.RemoveField(
            model_name='wine',
            name='cata_olf_aroma_2',
        ),
        migrations.RemoveField(
            model_name='wine',
            name='cata_olf_aroma_3',
        ),
        migrations.AddField(
            model_name='wine',
            name='cata_aspecto',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(0, 'Limpio'), (1, 'Brillante'), (2, 'Cristalino'), (3, 'Turbio'), (4, 'Velado')], max_length=10, null=True, verbose_name='Aspecto'),
        ),
        migrations.AddField(
            model_name='wine',
            name='cata_capa',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(0, 'Alta'), (1, 'Media'), (2, 'Baja')], max_length=10, null=True, verbose_name='Capa'),
        ),
        migrations.AddField(
            model_name='wine',
            name='cata_gust_sensacion',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(0, 'Dulce'), (1, 'Salado'), (2, 'Amargo'), (3, 'Ácido'), (3, 'Astringente'), (3, 'Cálido'), (3, 'Acuoso')], max_length=20, null=True, verbose_name='Sensacion'),
        ),
        migrations.AddField(
            model_name='wine',
            name='cata_gust_valoracion',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(0, 'Dulce'), (1, 'Salado'), (2, 'Amargo'), (3, 'Ácido'), (3, 'Astringente'), (3, 'Cálido'), (3, 'Acuoso')], max_length=20, null=True, verbose_name='Valoración'),
        ),
        migrations.AddField(
            model_name='wine',
            name='cata_olf_aroma',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(0, 'Florales'), (1, 'Flor blanca'), (2, 'Clavel'), (3, 'Violeta'), (4, 'Rosa'), (5, 'Afrutados'), (6, 'Manzana'), (7, 'Pera'), (8, 'Melocotón'), (9, 'Albaricoque'), (10, 'Cítricos'), (11, 'Frutas tropicales'), (12, 'Cereza'), (13, 'Frutos rojos'), (14, 'Frutos negros'), (15, 'Membrillo'), (16, 'Vegetales'), (17, 'Hinojo'), (18, 'Pimiento verde'), (19, 'Trufa'), (20, 'Hojarasca'), (21, 'Especias'), (22, 'Pimienta'), (23, 'Canela'), (24, 'Clavo'), (25, 'Coco'), (26, 'Mineral'), (27, 'Tiza'), (28, 'Yeso'), (29, 'Grafito'), (30, 'Yodo'), (31, 'Pedernal'), (32, 'Sílice'), (33, 'Lácticos'), (34, 'Mantequilla'), (35, 'Yogur'), (36, 'Levadura'), (37, 'Miga de pan'), (38, 'Azufroso'), (39, 'Barniz'), (40, 'Laca de uñas'), (41, 'Caramelo'), (42, 'Madera'), (43, 'Tabaco'), (44, 'Frutos secos'), (45, 'Cuero'), (46, 'Vainilla'), (47, 'Café'), (48, 'Tostados')], max_length=200, null=True, verbose_name='Aroma'),
        ),
        migrations.AddField(
            model_name='wine',
            name='cata_ribete',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(0, 'Transparente'), (1, 'Amarillo'), (2, 'Rosa'), (3, 'Violáceo'), (4, 'Azul'), (5, 'Rojo'), (6, 'Granate'), (7, 'Teja')], max_length=20, null=True, verbose_name='Ribete'),
        ),
        migrations.AlterField(
            model_name='wine',
            name='cata_color_blanco',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(0, 'Pálido'), (1, 'Verdoso'), (2, 'Limón'), (3, 'Pajizo'), (4, 'Oro'), (5, 'Dorado'), (6, 'Ámbar')], max_length=20, null=True, verbose_name='Tonalidades del Color (Blanco)'),
        ),
        migrations.AlterField(
            model_name='wine',
            name='cata_color_rosado',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(0, 'Pálido'), (1, 'Claro'), (2, 'Frambuesa'), (3, 'Fresa'), (4, 'Salmón'), (5, 'Anaranjado')], max_length=20, null=True, verbose_name='Tonalidades del Color (Rosado)'),
        ),
        migrations.AlterField(
            model_name='wine',
            name='cata_color_tinto',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(0, 'Violáceo'), (1, 'Rubí'), (2, 'Granate'), (3, 'Cereza'), (4, 'Teja'), (5, 'Picota'), (6, 'Caoba')], max_length=20, null=True, verbose_name='Tonalidades del Color (Tinto)'),
        ),
        migrations.AlterField(
            model_name='wine',
            name='cata_efervescencia',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(0, 'Tranquilo'), (1, 'Aguja'), (2, 'Burbujas finas'), (3, 'Burbujas grandes'), (4, 'Rosarios escasos'), (5, 'Rosarios medios'), (6, 'Rosarios abundantes'), (7, 'Corona'), (8, 'Sin corona')], max_length=20, null=True, verbose_name='Efervescencia'),
        ),
        migrations.AlterField(
            model_name='wine',
            name='cata_fluidez',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(0, 'Fluido'), (1, 'Glicérico'), (2, 'Untuoso'), (3, 'Graso'), (4, 'Viscoso')], max_length=20, null=True, verbose_name='Fluidez'),
        ),
        migrations.AlterField(
            model_name='wine',
            name='cata_gust_ataque',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(0, 'Malo'), (1, 'Ordinario'), (2, 'Placentero'), (3, 'Muy agradable')], max_length=20, null=True, verbose_name='Ataque'),
        ),
        migrations.AlterField(
            model_name='wine',
            name='cata_gust_persistencia',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(0, 'Alta'), (1, 'Media'), (2, 'Baja')], max_length=20, null=True, verbose_name='Persistencia'),
        ),
        migrations.AlterField(
            model_name='wine',
            name='cata_olf_intensidad',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(0, 'Inexistente'), (1, 'Débil'), (2, 'Media'), (3, 'Intensa'), (4, 'Potente')], max_length=20, null=True, verbose_name='Intensidad'),
        ),
    ]