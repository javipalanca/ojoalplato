from django.forms import ModelForm
from easy_select2 import Select2Multiple
from haystack.forms import SearchForm
from multiselectfield.forms.fields import MultiSelectFormField

from . import WINE_KIND_CHOICES, \
    CATA_TONALIDADES_BLANCO, CATA_TONALIDADES_ROSADO, CATA_TONALIDADES_TINTO, CATA_FLUIDEZ, CATA_EFERVESCENCIA, \
    CATA_OLFATIVA_INTENSIDAD, CATA_GUSTATIVA_ATAQUE, CATA_GUSTATIVA_PERSISTENCIA, CATA_ASPECTO, CATA_CAPA, CATA_RIBETE, \
    CATA_OLFATIVA_AROMA, CATA_GUSTATIVA_SENSACION, CATA_VALORACION
from .models import Wine


class RestaurantSearchForm(SearchForm):

    def no_query_found(self):
        return self.searchqueryset.all()


class WineForm(ModelForm):
    kind = MultiSelectFormField(label="Tipo",
                                widget=Select2Multiple(select2attrs={'width': '250px'}),
                                choices=WINE_KIND_CHOICES,
                                required=False
                                )
    cata_aspecto = MultiSelectFormField(label="Aspecto",
                                        widget=Select2Multiple(select2attrs={'width': '250px'}),
                                        choices=CATA_ASPECTO,
                                        required=False
                                        )
    cata_capa = MultiSelectFormField(label="Capa",
                                     widget=Select2Multiple(select2attrs={'width': '250px'}),
                                     choices=CATA_CAPA,
                                     required=False
                                     )
    cata_color_blanco = MultiSelectFormField(label="Tonalidades de colro (Blanco)",
                                             widget=Select2Multiple(select2attrs={'width': '250px'}),
                                             choices=CATA_TONALIDADES_BLANCO,
                                             required=False
                                             )
    cata_color_rosado = MultiSelectFormField(label="Tonalidades de color (Rosado)",
                                             widget=Select2Multiple(select2attrs={'width': '250px'}),
                                             choices=CATA_TONALIDADES_ROSADO,
                                             required=False
                                             )
    cata_color_tinto = MultiSelectFormField(label="Tonalidades de color (Tinto)",
                                            widget=Select2Multiple(select2attrs={'width': '250px'}),
                                            choices=CATA_TONALIDADES_TINTO,
                                            required=False
                                            )
    cata_ribete = MultiSelectFormField(label="Ribete",
                                       widget=Select2Multiple(select2attrs={'width': '250px'}),
                                       choices=CATA_RIBETE,
                                       required=False
                                       )
    cata_fluidez = MultiSelectFormField(label="Fluidez",
                                        widget=Select2Multiple(select2attrs={'width': '250px'}),
                                        choices=CATA_FLUIDEZ,
                                        required=False
                                        )
    cata_efervescencia = MultiSelectFormField(label="Efervescencia",
                                              widget=Select2Multiple(select2attrs={'width': '250px'}),
                                              choices=CATA_EFERVESCENCIA,
                                              required=False
                                              )
    cata_olf_intensidad = MultiSelectFormField(label="Intensidad aromática",
                                               widget=Select2Multiple(select2attrs={'width': '250px'}),
                                               choices=CATA_OLFATIVA_INTENSIDAD,
                                               required=False
                                               )
    cata_olf_aroma = MultiSelectFormField(label="Aroma",
                                          widget=Select2Multiple(select2attrs={'width': '250px'}),
                                          choices=CATA_OLFATIVA_AROMA,
                                          required=False
                                          )

    cata_gust_ataque = MultiSelectFormField(label="Ataque",
                                            widget=Select2Multiple(select2attrs={'width': '250px'}),
                                            choices=CATA_GUSTATIVA_ATAQUE,
                                            required=False
                                            )
    cata_gust_sensacion = MultiSelectFormField(label="Sensación",
                                               widget=Select2Multiple(select2attrs={'width': '250px'}),
                                               choices=CATA_GUSTATIVA_SENSACION,
                                               required=False
                                               )

    cata_gust_persistencia = MultiSelectFormField(label="Persistencia",
                                                  widget=Select2Multiple(select2attrs={'width': '250px'}),
                                                  choices=CATA_GUSTATIVA_PERSISTENCIA,
                                                  required=False
                                                  )
    cata_gust_valoracion = MultiSelectFormField(label="Valoración",
                                                widget=Select2Multiple(select2attrs={'width': '250px'}),
                                                choices=CATA_VALORACION,
                                                required=False
                                                )

    class Meta:
        model = Wine
        fields = "__all__"
