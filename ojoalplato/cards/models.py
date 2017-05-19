from autoslug import AutoSlugField
from copy import copy
from bs4 import BeautifulSoup

from django.conf import settings
from django.contrib.gis.db.models import PointField
from django.contrib.gis.gdal import CoordTransform
from django.contrib.gis.gdal import SpatialReference
from django.core.validators import validate_comma_separated_integer_list
from django.db.models import CharField, DateField, TextField, URLField, PositiveSmallIntegerField,\
    BooleanField, ImageField
from phonenumber_field.modelfields import PhoneNumberField
from model_utils.models import TimeStampedModel

from likert_field.models import LikertField
from taggit_autosuggest.managers import TaggableManager
from hitcount.models import HitCountMixin

from . import DEFAULT_PROJECTED_SRID, WINE_KIND_CHOICES, DEFAULT_WGS84_SRID


class Card(HitCountMixin):
    name = CharField(verbose_name="Nombre", max_length=200)
    slug = AutoSlugField(populate_from='name', verbose_name="slug", max_length=200, blank=True, null=True)

    image_header = ImageField(
        verbose_name="Imagen de cabecera",
        help_text="Imagen",
        upload_to=settings.MEDIA_ROOT,
        null=True, blank=True, )

    def get_posts_images(self):
        images = []
        for post in self.post_set:
            soup = BeautifulSoup(post.content, "html.parser")
            for img in soup.find_all('img'):
                if img:
                    images.append(img.attrs["src"])
        return images

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Restaurant(TimeStampedModel, Card):
    address = CharField(verbose_name="Dirección", max_length=300, blank=True, null=True)
    phone = PhoneNumberField(verbose_name="Teléfono", blank=True, null=True)
    url = URLField(verbose_name="Web", blank=True, null=True)
    last_visit = DateField(verbose_name="Fecha última visita", blank=True, null=True)
    price = CharField(verbose_name="Precio sin vino", max_length=50, blank=True, null=True)
    avg_price = PositiveSmallIntegerField(verbose_name="Precio medio", blank=True, null=True)
    menu_price = PositiveSmallIntegerField(verbose_name="Precio de menú", blank=True, null=True)
    location = PointField(srid=DEFAULT_PROJECTED_SRID, verbose_name="Posición en el mapa", blank=True, null=True)
    stars = LikertField(verbose_name="Estrellas michelín", blank=True)
    freedays = CharField(verbose_name="Días cerrado",
                         validators=[validate_comma_separated_integer_list],
                         max_length=80, blank=True, null=True)
    is_closed = BooleanField(verbose_name="Restaurante cerrado", default=False)
    notes = TextField(verbose_name="Notas", blank=True, null=True)

    def get_position_wgs84(self):
        """Transforms position to WGS-84 system."""
        destination_coord = SpatialReference(DEFAULT_WGS84_SRID)
        origin_coord = SpatialReference(DEFAULT_PROJECTED_SRID)
        trans = CoordTransform(origin_coord, destination_coord)
        # Copy transformed point...
        position = copy(self.location)
        position.transform(trans)
        return [position[1], position[0]]

    def get_absolute_url(self):
        return reverse("restaurant-detail", args=[self.slug])

    class Meta:
        verbose_name = "Restaurante"
        verbose_name_plural = "Restaurantes"


class Wine(TimeStampedModel, Card):
    kind = CharField(verbose_name="Tipo", max_length=50, choices=WINE_KIND_CHOICES)
    last_taste = DateField(verbose_name="Fecha última cata", blank=True, null=True)
    price = CharField(verbose_name="Precio medio", max_length=50, blank=True, null=True)
    opinion = TextField(verbose_name="Opinión", blank=True, null=True)

    class Meta:
        verbose_name = "Vino"
        verbose_name_plural = "Vinos"


class Recipe(TimeStampedModel, Card):
    ingredients = TaggableManager(verbose_name="Ingredientes",
                                  help_text="Lista de ingredientes separados por comas.",
                                  blank=True)
    content = TextField(verbose_name="Elaboración", blank=True, null=True)

    class Meta:
        verbose_name = "Receta"
        verbose_name_plural = "Recetas"
