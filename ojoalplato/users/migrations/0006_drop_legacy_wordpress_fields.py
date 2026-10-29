# Limpieza de deuda histórica: elimina las columnas legacy del modelo User
# importado de WordPress (activation_key, login, status, url, UserMeta),
# que ya no existen en ojoalplato.users.models.User y rompen la creación
# del AnonymousUser de django-guardian en instalaciones limpias.

from django.db import migrations


def drop_column_if_exists(schema_editor, table, column):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            "SELECT 1 FROM information_schema.columns WHERE table_name=%s AND column_name=%s",
            [table, column],
        )
        if cursor.fetchone():
            cursor.execute(f'ALTER TABLE "{table}" DROP COLUMN "{column}"')


def drop_table_if_exists(schema_editor, table):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            "SELECT 1 FROM information_schema.tables WHERE table_name=%s",
            [table],
        )
        if cursor.fetchone():
            cursor.execute(f'DROP TABLE "{table}" CASCADE')


def drop_legacy(apps, schema_editor):
    drop_table_if_exists(schema_editor, "users_usermeta")
    for column in ("activation_key", "login", "status", "url"):
        drop_column_if_exists(schema_editor, "users_user", column)


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_merge_0004_auto_20210209_1852_0004_auto_20220828_1326'),
    ]

    operations = [
        migrations.RunPython(drop_legacy, migrations.RunPython.noop),
    ]
