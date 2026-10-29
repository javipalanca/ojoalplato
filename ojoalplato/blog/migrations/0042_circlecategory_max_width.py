# Añade max_width a CircleCategory y lo aplica a las dos categorías
# que en el diseño original ocupaban dos líneas.

from django.db import migrations, models


def set_max_width(apps, schema_editor):
    CircleCategory = apps.get_model('blog', 'CircleCategory')
    CircleCategory.objects.filter(name__in=["Mapa y Guías", "Categorías y Etiquetas"]).update(max_width=128)


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0041_sitesettings_site_since_menuitem_circlecategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='circlecategory',
            name='max_width',
            field=models.PositiveSmallIntegerField(blank=True, help_text="Opcional. Limita el ancho del texto para que salte a dos líneas (p.ej. 128 en 'Mapa y Guías' y 'Categorías y Etiquetas').", null=True, verbose_name='Ancho máximo del texto (px)'),
        ),
        migrations.RunPython(set_max_width, migrations.RunPython.noop),
    ]
