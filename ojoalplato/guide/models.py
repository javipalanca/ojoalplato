from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse
from hitcount.models import HitCountMixin
from model_utils.models import TimeStampedModel

from ojoalplato.cards.models import Restaurant


class Guide(TimeStampedModel, HitCountMixin):
    """Guide model."""

    title = models.CharField(max_length=255, verbose_name="Título")
    city = models.CharField(max_length=255, verbose_name="Ciudad")
    slug = AutoSlugField(populate_from='title', verbose_name="slug", max_length=200)
    introduction = models.TextField(blank=True, verbose_name="Introducción")
    image = models.ImageField(upload_to='guides', verbose_name="Imagen de portada",
                              help_text="Imagen", blank=True)
    restaurants = models.ManyToManyField(Restaurant, related_name='guides', verbose_name="Restaurantes")

    class Meta:
        """Meta class."""
        verbose_name = "Guía"
        verbose_name_plural = "Guías"
        ordering = ('-created',)

    def __str__(self):
        """Return title and username."""
        return '{}'.format(self.title)

    def get_absolute_url(self):
        """Return slug."""
        return reverse('guides:guide-detail', kwargs={'slug': self.slug})
