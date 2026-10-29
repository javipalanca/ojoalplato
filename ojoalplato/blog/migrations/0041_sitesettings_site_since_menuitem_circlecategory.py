# Añade site_since a SiteSettings y crea los modelos MenuItem y
# CircleCategory, sembrados con los datos que reproducen el aspecto actual.

from django.db import migrations, models


def seed_defaults(apps, schema_editor):
    MenuItem = apps.get_model('blog', 'MenuItem')
    CircleCategory = apps.get_model('blog', 'CircleCategory')

    menu_items = [
        ("Inicio", "/", 0),
        ("Contacto", "/contact/", 1),
        ("Suscribirse", "/subscription/ojoalplato/", 2),
        ("Curso de cata de vinos", "/curso-rapido-de-cata-de-vinos/", 3),
        ("Comida del millón", "/la-celebracion-del-millon-de-ojoalplato/", 4),
        ("Sobre mí", "/sobre-mi/", 5),
    ]
    for label, url, order in menu_items:
        MenuItem.objects.get_or_create(
            label=label, defaults={"url": url, "order": order, "active": True}
        )

    circles = [
        ("Mapa y Guías", "/map/", "images/fork_map.png", 0),
        ("Restaurantes", "/category/restaurantes/", "wpfamily/img/cuberteria.jpg", 1),
        ("Vinos", "/category/vinos/", "wpfamily/img/wine.jpg", 2),
        ("Recetas", "/category/recetas/", "wpfamily/img/recipe.jpg", 3),
        ("Cervezas", "/category/cervezas/", "wpfamily/img/beer.jpg", 4),
        ("Categorías y Etiquetas", "/categories/and/tags/", "wpfamily/img/plus_ic3.png", 5),
    ]
    for name, url, image_static, order in circles:
        CircleCategory.objects.get_or_create(
            name=name,
            defaults={"url": url, "image_static": image_static, "order": order, "active": True},
        )


def unseed_defaults(apps, schema_editor):
    apps.get_model('blog', 'MenuItem').objects.all().delete()
    apps.get_model('blog', 'CircleCategory').objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0040_sitesettings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='termtaxonomyrelationship',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='site_since',
            field=models.CharField(blank=True, default='Desde 2008', max_length=100, verbose_name='Texto bajo el logo'),
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100, verbose_name='Etiqueta')),
                ('url', models.CharField(help_text='Ruta interna (p.ej. /contact/) o URL absoluta.', max_length=300, verbose_name='URL')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name='Orden')),
                ('active', models.BooleanField(default=True, verbose_name='Activa')),
            ],
            options={
                'verbose_name': 'Entrada de menú',
                'verbose_name_plural': 'Entradas de menú',
                'ordering': ['order', 'id'],
            },
        ),
        migrations.CreateModel(
            name='CircleCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('url', models.CharField(help_text='Ruta interna (p.ej. /map/) o URL absoluta.', max_length=300, verbose_name='URL')),
                ('image', models.ImageField(blank=True, help_text='Imagen circular de la categoría. Si no se sube ninguna, se usa la imagen estática.', null=True, upload_to='site/circles/', verbose_name='Imagen')),
                ('image_static', models.CharField(blank=True, help_text='Ruta dentro de static/ (p.ej. wpfamily/img/wine.jpg) a usar si no hay imagen subida.', max_length=200, verbose_name='Imagen estática')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name='Orden')),
                ('active', models.BooleanField(default=True, verbose_name='Activa')),
            ],
            options={
                'verbose_name': 'Categoría circular',
                'verbose_name_plural': 'Categorías circulares',
                'ordering': ['order', 'id'],
            },
        ),
        migrations.RunPython(seed_defaults, unseed_defaults),
    ]
