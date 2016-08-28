from django.contrib.gis.db.models import PointField
from django.core.validators import validate_comma_separated_integer_list
from django.db.models import CharField, DateField, TextField, URLField, PositiveSmallIntegerField, BooleanField
from likert_field.models import LikertField
from phonenumber_field.modelfields import PhoneNumberField
from model_utils.models import TimeStampedModel
from taggit_autosuggest.managers import TaggableManager

from . import DEFAULT_PROJECTED_SRID, WINE_KIND_CHOICES, DAY_CHOICES


class Restaurant(TimeStampedModel):
    name = CharField(verbose_name="Nombre", max_length=200)
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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Restaurante"
        verbose_name_plural = "Restaurantes"


class Wine(TimeStampedModel):
    name = CharField(verbose_name="Nombre", max_length=200)
    kind = CharField(verbose_name="Tipo", max_length=50, choices=WINE_KIND_CHOICES)
    last_taste = DateField(verbose_name="Fecha última cata", blank=True, null=True)
    price = CharField(verbose_name="Precio medio", max_length=50, blank=True, null=True)
    opinion = TextField(verbose_name="Opinión", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Vino"
        verbose_name_plural = "Vinos"


class Recipe(TimeStampedModel):
    name = CharField(verbose_name="Nombre", max_length=200)
    ingredients = TaggableManager(verbose_name="Ingredientes",
                                  help_text="Lista de ingredientes separados por comas.",
                                  blank=True)
    content = TextField(verbose_name="Elaboración", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Receta"
        verbose_name_plural = "Recetas"
