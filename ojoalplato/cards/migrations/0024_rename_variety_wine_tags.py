# Generated by Django 3.2.13 on 2022-08-28 20:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0023_taggedvariety_content_object'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wine',
            old_name='variety',
            new_name='tags',
        ),
    ]