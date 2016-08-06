# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-05 17:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('parent_id', models.IntegerField(default=0)),
                ('author_name', models.CharField(max_length=255)),
                ('author_email', models.EmailField(max_length=100)),
                ('author_url', models.URLField(blank=True)),
                ('author_ip', models.GenericIPAddressField(blank=True, null=True)),
                ('post_date', models.DateTimeField()),
                ('content', models.TextField()),
                ('karma', models.IntegerField()),
                ('approved', models.CharField(max_length=20)),
                ('agent', models.CharField(max_length=255)),
                ('comment_type', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ['-post_date'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('guid', models.CharField(max_length=255)),
                ('post_type', models.CharField(choices=[('attachment', 'attachment'), ('page', 'page'), ('post', 'post'), ('revision', 'revision')], max_length=20)),
                ('status', models.CharField(choices=[('draft', 'draft'), ('inherit', 'inherit'), ('private', 'private'), ('publish', 'publish')], max_length=20)),
                ('title', models.TextField()),
                ('slug', models.SlugField(max_length=200)),
                ('excerpt', models.TextField()),
                ('content', models.TextField()),
                ('content_filtered', models.TextField()),
                ('post_date', models.DateTimeField()),
                ('modified', models.DateTimeField()),
                ('comment_status', models.CharField(choices=[('closed', 'closed'), ('open', 'open')], max_length=20)),
                ('comment_count', models.IntegerField(default=0)),
                ('ping_status', models.CharField(choices=[('closed', 'closed'), ('open', 'open')], max_length=20)),
                ('to_ping', models.TextField()),
                ('pinged', models.TextField()),
                ('password', models.CharField(max_length=20)),
                ('parent_id', models.IntegerField(default=0)),
                ('menu_order', models.IntegerField(default=0)),
                ('mime_type', models.CharField(max_length=100)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-post_date'],
                'get_latest_by': 'post_date',
            },
        ),
        migrations.CreateModel(
            name='PostMeta',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('key', models.CharField(max_length=255)),
                ('value', models.TextField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meta', to='blog.Post')),
            ],
        ),
        migrations.CreateModel(
            name='Taxonomy',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32)),
                ('description', models.TextField()),
                ('parent_id', models.IntegerField(default=0)),
                ('count', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.CharField(max_length=200)),
                ('group', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TermTaxonomyRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Post')),
                ('term_taxonomy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relationships', to='blog.Taxonomy')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.AddField(
            model_name='taxonomy',
            name='term',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='taxonomies', to='blog.Term'),
        ),
        migrations.AddField(
            model_name='post',
            name='terms',
            field=models.ManyToManyField(blank=True, through='blog.TermTaxonomyRelationship', to='blog.Taxonomy'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.Post'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
    ]
