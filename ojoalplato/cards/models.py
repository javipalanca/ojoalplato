from copy import copy

from autoslug import AutoSlugField
from bs4 import BeautifulSoup
from django.contrib.gis.db.models import PointField
from django.contrib.gis.gdal import CoordTransform, SpatialReference
from django.contrib.gis.geos import Point
from django.core.validators import validate_comma_separated_integer_list
from django.db.models import CharField, DateField, TextField, URLField, \
    BooleanField, ImageField, EmailField, ForeignKey, CASCADE, IntegerField
from django.urls import reverse
from hitcount.models import HitCountMixin
from likert_field.models import LikertField
from model_utils.models import TimeStampedModel
from multiselectfield import MultiSelectField
from phonenumber_field.modelfields import PhoneNumberField
from taggit.models import TaggedItemBase, TagBase
from taggit_autosuggest.managers import TaggableManager

from ojoalplato.blog.templatetags.content_filters import media
from . import DEFAULT_PROJECTED_SRID, WINE_KIND_CHOICES, DEFAULT_WGS84_SRID, CATA_LIMPIDEZ, CATA_INTENSIDAD, \
    CATA_TONALIDADES_BLANCO, CATA_TONALIDADES_ROSADO, CATA_TONALIDADES_TINTO, CATA_FLUIDEZ, CATA_EFERVESCENCIA, \
    CATA_OLFATIVA_1IMPRESION, CATA_OLFATIVA_INTENSIDAD, CATA_OLFATIVA_AROMA_PRIMARIOS, CATA_OLFATIVA_AROMA_SECUNDARIOS, \
    CATA_OLFATIVA_AROMA_TERCIARIOS, CATA_GUSTATIVA_ATAQUE, CATA_GUSTATIVA_DULZOR, CATA_GUSTATIVA_ALCOHOL, CATA_GUSTATIVA_ACIDEZ, \
    CATA_GUSTATIVA_TANINO, CATA_GUSTATIVA_CUERPO, CATA_GUSTATIVA_BOCA, CATA_GUSTATIVA_PERSISTENCIA, VIEW_ICON, SMELL_ICON, \
    TASTE_ICON


class TaggedRestaurantTag(TaggedItemBase):
    content_object = ForeignKey('Restaurant', on_delete=CASCADE)


class Restaurant(TimeStampedModel, HitCountMixin):
    name = CharField(verbose_name="Nombre", max_length=200)
    slug = AutoSlugField(populate_from='name', verbose_name="slug", max_length=200, blank=True, null=True)
    chef = CharField(verbose_name="Cocinero/a", max_length=200, blank=True, null=True)
    sumiller = CharField(verbose_name="Sumiller", max_length=200, blank=True, null=True)
    manager = CharField(verbose_name="Jefe/a de Sala", max_length=200, blank=True, null=True)
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
                           through=TaggedRestaurantTag,
                           blank=True)

    image_header = ImageField(
        verbose_name="Imagen de cabecera",
        help_text="Imagen",
        upload_to=".",  # settings.MEDIA_ROOT,
        null=True, blank=True, )

    def title(self):
        return self.name

    @property
    def img_src(self):
        if self.image_header and hasattr(self.image_header, 'url'):
            url = self.image_header.url.replace("//media", "/media")
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
                result = media(img.attrs["src"])
        return result

    @property
    def absolute_url(self):
        return self.get_absolute_url()

    @property
    def autocomplete_text(self):
        text = "{} {} {} {}".format(self.name, self.chef, self.address, self.awards)
        tags = " ".join([tag.name for tag in self.tags.all()])
        return " ".join([text, tags])

    def get_posts_images(self):
        images = []
        for post in self.posts.all():
            soup = BeautifulSoup(post.content, "html.parser")
            for img in soup.find_all('img'):
                if img:
                    images.append(media(img.attrs["src"]))
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
            return [position[0], position[1]]
        else:
            return [None, None]

    @property
    def location_wgs84(self):
        lon, lat = self.get_position_wgs84()
        if lon and lat:
            return Point(lat, lon)
        else:
            return None

    @property
    def location_wgs84_reverse(self):
        # this is needed for elasticsearch, since it changes lat/lon order
        lon, lat = self.get_position_wgs84()
        if lon and lat:
            return Point(lon, lat)
        else:
            return None

    def google_maps_url(self):
        point = self.get_position_wgs84()
        return "http://www.google.com/maps/place/{},{}".format(point[1], point[0])

    def get_absolute_url(self):
        return reverse("cards:restaurant-detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Restaurante"
        verbose_name_plural = "Restaurantes"
        ordering = ['name']

    def __str__(self):
        return self.name


class Winery(TimeStampedModel, HitCountMixin):
    name = CharField(verbose_name="Nombre de Bodega", max_length=80)
    url = URLField(verbose_name="Web", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Bodega"
        verbose_name_plural = "Bodegas"
        ordering = ['name']


class VarietyTag(TagBase):
    class Meta:
        verbose_name = "Variedad"
        verbose_name_plural = "Variedades"


class TaggedVariety(TaggedItemBase):
    tag = ForeignKey(VarietyTag, on_delete=CASCADE, related_name="%(app_label)s_%(class)s_items")
    content_object = ForeignKey('Wine', on_delete=CASCADE)


class Wine(TimeStampedModel, HitCountMixin):
    name = CharField(verbose_name="Nombre", max_length=200)
    slug = AutoSlugField(populate_from='name', verbose_name="slug", max_length=200, blank=True, null=True)
    winery = ForeignKey(Winery, verbose_name="Bodega", on_delete=CASCADE, blank=True, null=True)
    year = IntegerField(verbose_name="Añada", max_length=5, blank=True, null=True)
    kind = MultiSelectField(verbose_name="Tipo", choices=WINE_KIND_CHOICES, max_length=10, blank=True, null=True)
    country = CharField(verbose_name="País", max_length=50, blank=True, null=True)
    region = CharField(verbose_name="Región", max_length=50, blank=True, null=True)
    tags = TaggableManager(verbose_name="Variedades",
                           help_text="Lista de variedades de uva separadas por comas.",
                           through=TaggedVariety,
                           blank=True)
    preparation = CharField(verbose_name="Elaboración", max_length=50, blank=True, null=True)
    last_taste = DateField(verbose_name="Fecha última cata", blank=True, null=True)
    price = CharField(verbose_name="Precio medio", max_length=50, blank=True, null=True)
    other = TextField(verbose_name="Otros datos", blank=True, null=True)
    opinion = TextField(verbose_name="Opinión", blank=True, null=True)

    parker_points = IntegerField(verbose_name="Puntos Parker", blank=True, null=True)
    penyin_points = IntegerField(verbose_name="Puntos Peñin", blank=True, null=True)

    image_bottle = ImageField(
        verbose_name="Imagen de la botella",
        help_text="Imagen de la botella",
        upload_to=".",  # settings.MEDIA_ROOT,
        null=True, blank=True, )

    image_header = ImageField(
        verbose_name="Imagen de la etiqueta",
        help_text="Imagen de la etiqueta",
        upload_to=".",  # settings.MEDIA_ROOT,
        null=True, blank=True, )

    show_tasting_form = BooleanField(verbose_name="Mostrar Ficha de cata", default=False)

    cata_limpidez = MultiSelectField(verbose_name="Limpidez", choices=CATA_LIMPIDEZ, max_length=10, blank=True, null=True)
    cata_intensidad = MultiSelectField(verbose_name="Intensidad", choices=CATA_INTENSIDAD, max_length=10, blank=True, null=True)
    cata_color_blanco = MultiSelectField(verbose_name="Tonalidades del Color (Blanco)", choices=CATA_TONALIDADES_BLANCO,
                                         max_length=10, blank=True, null=True)
    cata_color_rosado = MultiSelectField(verbose_name="Tonalidades del Color (Rosado)", choices=CATA_TONALIDADES_ROSADO,
                                         max_length=10, blank=True, null=True)
    cata_color_tinto = MultiSelectField(verbose_name="Tonalidades del Color (Tinto)", choices=CATA_TONALIDADES_TINTO,
                                        max_length=10, blank=True, null=True)
    cata_fluidez = MultiSelectField(verbose_name="Fluidez", choices=CATA_FLUIDEZ, max_length=10, blank=True, null=True)
    cata_efervescencia = MultiSelectField(verbose_name="Efervescencia", choices=CATA_EFERVESCENCIA, max_length=10, blank=True,
                                          null=True)
    cata_olf_1a = MultiSelectField(verbose_name="1ª Impresión", choices=CATA_OLFATIVA_1IMPRESION, max_length=10, blank=True,
                                   null=True)
    cata_olf_intensidad = MultiSelectField(verbose_name="Intensidad", choices=CATA_OLFATIVA_INTENSIDAD, max_length=10, blank=True,
                                           null=True)
    cata_olf_aroma_1 = MultiSelectField(verbose_name="Aroma (Carácter) Primarios (cepa)", choices=CATA_OLFATIVA_AROMA_PRIMARIOS,
                                        max_length=10, blank=True, null=True)
    cata_olf_aroma_2 = MultiSelectField(verbose_name="Aroma (Carácter) Secundarios (fermentación)",
                                        choices=CATA_OLFATIVA_AROMA_SECUNDARIOS, max_length=10, blank=True, null=True)
    cata_olf_aroma_3 = MultiSelectField(verbose_name="Aroma (Carácter) Terciarios (maduración)",
                                        choices=CATA_OLFATIVA_AROMA_TERCIARIOS, max_length=10, blank=True, null=True)
    cata_gust_ataque = MultiSelectField(verbose_name="Ataque", choices=CATA_GUSTATIVA_ATAQUE, max_length=10, blank=True,
                                        null=True)
    cata_gust_dulzor = MultiSelectField(verbose_name="Dulzor", choices=CATA_GUSTATIVA_DULZOR, max_length=10, blank=True,
                                        null=True)
    cata_gust_alcohol = MultiSelectField(verbose_name="Alcohol", choices=CATA_GUSTATIVA_ALCOHOL, max_length=10, blank=True,
                                         null=True)
    cata_gust_acidez = MultiSelectField(verbose_name="Acidez", choices=CATA_GUSTATIVA_ACIDEZ, max_length=10, blank=True,
                                        null=True)
    cata_gust_tanino = MultiSelectField(verbose_name="Tanino", choices=CATA_GUSTATIVA_TANINO, max_length=10, blank=True,
                                        null=True)
    cata_gust_cuerpo = MultiSelectField(verbose_name="Cuerpo", choices=CATA_GUSTATIVA_CUERPO, max_length=10, blank=True,
                                        null=True)
    cata_gust_boca = MultiSelectField(verbose_name="Paso en boca", choices=CATA_GUSTATIVA_BOCA, max_length=10, blank=True,
                                      null=True)
    cata_gust_persistencia = MultiSelectField(verbose_name="Persistencia", choices=CATA_GUSTATIVA_PERSISTENCIA, max_length=10,
                                              blank=True, null=True)

    @staticmethod
    def get_view_icon():
        return VIEW_ICON

    @staticmethod
    def get_smell_icon():
        return SMELL_ICON

    @staticmethod
    def get_taste_icon():
        return TASTE_ICON

    def get_absolute_url(self):
        return reverse("cards:wine-detail", kwargs={"slug": self.slug})

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
        upload_to=".",  # settings.MEDIA_ROOT,
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
