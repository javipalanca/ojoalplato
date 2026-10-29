# Corrige la URL de la categoría circular "Mapa y Guías": el mapa vive en
# /cards/map/ (namespace cards:map-list), no en /map/.

from django.db import migrations


def fix_map_url(apps, schema_editor):
    CircleCategory = apps.get_model('blog', 'CircleCategory')
    CircleCategory.objects.filter(name="Mapa y Guías", url="/map/").update(url="/cards/map/")


def revert_map_url(apps, schema_editor):
    CircleCategory = apps.get_model('blog', 'CircleCategory')
    CircleCategory.objects.filter(name="Mapa y Guías", url="/cards/map/").update(url="/map/")


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0042_circlecategory_max_width'),
    ]

    operations = [
        migrations.RunPython(fix_map_url, revert_map_url),
    ]
