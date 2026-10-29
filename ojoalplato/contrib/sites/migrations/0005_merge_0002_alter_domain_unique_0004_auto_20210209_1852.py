# Migración de merge para resolver las dos hojas de la app "sites":
#   - 0002_alter_domain_unique (stub que necesita django-newsletter
#     en una instalación limpia, porque referencia ese nodo)
#   - 0004_auto_20210209_1852 (cadena histórica ya aplicada en producción)
# Así el grafo queda consistente sin alterar el historial existente.

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('sites', '0004_auto_20210209_1852'),
    ]

    operations = [
    ]
