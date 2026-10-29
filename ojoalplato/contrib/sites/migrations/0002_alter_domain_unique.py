# -*- coding: utf-8 -*-
# Nodo de compatibilidad: django-newsletter (0013_submission_site) depende de
# sites.0002_alter_domain_unique. Como este proyecto sustituye las migraciones
# de "sites" (MIGRATION_MODULES) por las de contrib/sites, donde la 0002
# se llama "0002_set_site_domain_and_name", hay que crear este nodo intermedio
# para que el grafo de migraciones sea consistente.

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
    ]
