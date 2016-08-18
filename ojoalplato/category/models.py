from categories.models import CategoryBase, Category as Categories

from django.conf import settings
from django.contrib import admin
from django.db import models


class Category(CategoryBase):
    """
    A category
    """
    thumbnail = models.ImageField(
        upload_to=settings.MEDIA_ROOT,
        null=True, blank=True,)

    class Meta:
        verbose_name_plural = 'categories'

