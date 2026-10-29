# -*- coding: utf-8 -*-
# Nodo de compatibilidad: django-newsletter (0013_submission_site) depende de
# sites.0002_alter_domain_unique. Este proyecto sustituye las migraciones de
# "sites" (MIGRATION_MODULES) por las de contrib/sites, donde esa migración
# se llama "0002_set_site_domain_and_name" (e incorpora el cambio de dominio
# en la 0003). Se declara como squash (replaces) de la 0002 y 0003 originales
# para que, en bases de datos donde ya están aplicadas, Django la dé por
# satisfecha; y en instalaciones limpias se aplique como migración vacía.

from django.db import migrations


class Migration(migrations.Migration):

    replaces = [
        ('sites', '0002_set_site_domain_and_name'),
        ('sites', '0003_auto_20160805_1707'),
    ]

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
    ]
