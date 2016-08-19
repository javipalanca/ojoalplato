from categories.models import CategoryBase, Category as Categories

from django.conf import settings
from django.db import models


class Category(CategoryBase):
    """
    A category
    """
    thumbnail = models.ImageField(
        upload_to=settings.MEDIA_ROOT,
        default=settings.MEDIA_ROOT + "uncategorized.gif",
        null=True, blank=True,)

    def thumbnail_url(self):
        url = self.thumbnail.url
        relative = url.split(settings.MEDIA_ROOT)[1]
        if relative.startswith("/"):
            relative = relative[1:]
        return settings.MEDIA_URL + relative

    class Meta:
        verbose_name_plural = 'Categorías'
        verbose_name = 'Categoría'
