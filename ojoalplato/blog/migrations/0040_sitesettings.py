# Generated manually: SiteSettings singleton model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0039_alter_post_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(default='Ojo al plato', max_length=100, verbose_name='Nombre del sitio')),
                ('logo', models.ImageField(blank=True, help_text='Logo que aparece en la cabecera. PNG con fondo transparente recomendado.', null=True, upload_to='site/', verbose_name='Logo principal')),
                ('logo_alt', models.CharField(default='Ojo al plato', max_length=100, verbose_name='Texto alternativo del logo')),
            ],
            options={
                'verbose_name': 'Configuración del sitio',
                'verbose_name_plural': 'Configuración del sitio',
            },
        ),
    ]
