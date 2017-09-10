from autoslug import AutoSlugField
from copy import copy
from bs4 import BeautifulSoup

from django.conf import settings
from django.contrib.gis.db.models import PointField
from django.contrib.gis.gdal import CoordTransform
from django.contrib.gis.gdal import SpatialReference
from django.contrib.gis.geos import Point
from django.core.urlresolvers import reverse
from django.core.validators import validate_comma_separated_integer_list
from django.db.models import CharField, DateField, TextField, URLField, \
    BooleanField, ImageField, EmailField
from phonenumber_field.modelfields import PhoneNumberField
from model_utils.models import TimeStampedModel

from likert_field.models import LikertField
from taggit_autosuggest.managers import TaggableManager
from hitcount.models import HitCountMixin

from . import DEFAULT_PROJECTED_SRID, WINE_KIND_CHOICES, DEFAULT_WGS84_SRID


class Restaurant(TimeStampedModel, HitCountMixin):
    name = CharField(verbose_name="Nombre", max_length=200)
    slug = AutoSlugField(populate_from='name', verbose_name="slug", max_length=200, blank=True, null=True)
    chef = CharField(verbose_name="Cocinero", max_length=200, blank=True, null=True)
    address = CharField(verbose_name="Dirección", max_length=300, blank=True, null=True)
    phone = PhoneNumberField(verbose_name="Teléfono", blank=True, null=True)
    url = URLField(verbose_name="Web", blank=True, null=True)
    email = EmailField(verbose_name="E-mail", blank=True, null=True)
    last_visit = DateField(verbose_name="Fecha última visita", blank=True, null=True)
    price = CharField(verbose_name="Precio sin vino", max_length=50, blank=True, null=True)
    avg_price = CharField(verbose_name="Precio medio", max_length=50, blank=True, null=True)
    menu_price = CharField(verbose_name="Precio de menú", max_length=50, blank=True, null=True)
    location = PointField(srid=DEFAULT_PROJECTED_SRID, verbose_name="Posición en el mapa", blank=True, null=True)
    stars = LikertField(verbose_name="Estrellas michelín", default=0)
    suns = LikertField(verbose_name="Soles Repsol", default=0)
    awards = CharField(verbose_name="Distinciones", max_length=300, blank=True, null=True)
    freedays = CharField(verbose_name="Días cerrado",
                         validators=[validate_comma_separated_integer_list],
                         max_length=80, blank=True, null=True)
    is_closed = BooleanField(verbose_name="Restaurante cerrado", default=False)
    notes = TextField(verbose_name="Notas", blank=True, null=True)

    tags = TaggableManager(verbose_name="Etiquetas",
                           help_text="Lista de etiquetas separadas por comas.",
                           blank=True)

    image_header = ImageField(
        verbose_name="Imagen de cabecera",
        help_text="Imagen",
        upload_to=settings.MEDIA_ROOT,
        null=True, blank=True, )

    def title(self):
        return self.name

    @property
    def img_src(self):
        if self.image_header and hasattr(self.image_header, 'url'):
            split = "/media/"
            relative = self.image_header.url.split(split)[1]
            if relative.startswith("/"):
                relative = relative[1:]
            url = settings.MEDIA_URL + relative
        else:
            url = self.first_post_image()
        return url

    def first_post_image(self):
        result = "#"
        if self.posts.count() > 0:
            post = self.posts.first()
            soup = BeautifulSoup(post.content, "html.parser")
            img = soup.find('img')
            if img:
                result = img.attrs["src"]
        return result

    @property
    def absolute_url(self):
        return self.get_absolute_url()

    @property
    def autocomplete_text(self):
        text = "{} {} {}".format(self.name, self.chef, self.address)
        tags = " ".join([tag.name for tag in self.tags.all()])
        return " ".join([text, tags])

    def get_posts_images(self):
        images = []
        for post in self.posts.all():
            soup = BeautifulSoup(post.content, "html.parser")
            for img in soup.find_all('img'):
                if img:
                    images.append(img.attrs["src"])
        return images

    def get_position_wgs84(self):
        """Transforms position to WGS-84 system."""
        destination_coord = SpatialReference(DEFAULT_WGS84_SRID)
        origin_coord = SpatialReference(DEFAULT_PROJECTED_SRID)
        trans = CoordTransform(origin_coord, destination_coord)
        # Copy transformed point...
        position = copy(self.location)
        position.transform(trans)
        if position:
            return [position[1], position[0]]
        else:
            return [None, None]

    @property
    def location_wgs84(self):
        lat, lon = self.get_position_wgs84()
        if lat and lon:
            return Point(lat, lon)
        else:
            return None

    def google_maps_url(self):
        point = self.get_position_wgs84()
        return "http://www.google.com/maps/place/{},{}".format(point[0], point[1])

    def get_absolute_url(self):
        return reverse("cards:restaurant-detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Restaurante"
        verbose_name_plural = "Restaurantes"
        ordering = ['name']

    def __str__(self):
        return self.name


class Wine(TimeStampedModel, HitCountMixin):
    name = CharField(verbose_name="Nombre", max_length=200)
    slug = AutoSlugField(populate_from='name', verbose_name="slug", max_length=200, blank=True, null=True)
    kind = CharField(verbose_name="Tipo", max_length=50, choices=WINE_KIND_CHOICES)
    last_taste = DateField(verbose_name="Fecha última cata", blank=True, null=True)
    price = CharField(verbose_name="Precio medio", max_length=50, blank=True, null=True)
    opinion = TextField(verbose_name="Opinión", blank=True, null=True)

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
        verbose_name = "Vino"
        verbose_name_plural = "Vinos"
        ordering = ['name']


class Recipe(TimeStampedModel, HitCountMixin):
    name = CharField(verbose_name="Nombre", max_length=200)
    slug = AutoSlugField(populate_from='name', verbose_name="slug", max_length=200, blank=True, null=True)
    ingredients = TaggableManager(verbose_name="Ingredientes",
                                  help_text="Lista de ingredientes separados por comas.",
                                  blank=True)
    content = TextField(verbose_name="Elaboración", blank=True, null=True)
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
        verbose_name = "Receta"
        verbose_name_plural = "Recetas"
        ordering = ['name']
