from django.forms import ModelForm
from easy_select2 import Select2Multiple
from haystack.forms import SearchForm
from multiselectfield.forms.fields import MultiSelectFormField

from . import WINE_KIND_CHOICES, CATA_LIMPIDEZ, CATA_INTENSIDAD, \
    CATA_TONALIDADES_BLANCO, CATA_TONALIDADES_ROSADO, CATA_TONALIDADES_TINTO, CATA_FLUIDEZ, CATA_EFERVESCENCIA, \
    CATA_OLFATIVA_1IMPRESION, CATA_OLFATIVA_INTENSIDAD, CATA_OLFATIVA_AROMA_PRIMARIOS, CATA_OLFATIVA_AROMA_SECUNDARIOS, \
    CATA_OLFATIVA_AROMA_TERCIARIOS, CATA_GUSTATIVA_ATAQUE, CATA_GUSTATIVA_DULZOR, CATA_GUSTATIVA_ALCOHOL, CATA_GUSTATIVA_ACIDEZ, \
    CATA_GUSTATIVA_TANINO, CATA_GUSTATIVA_CUERPO, CATA_GUSTATIVA_BOCA, CATA_GUSTATIVA_PERSISTENCIA
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
    cata_limpidez = MultiSelectFormField(label="Limpidez",
                                         widget=Select2Multiple(select2attrs={'width': '250px'}),
                                         choices=CATA_LIMPIDEZ,
                                         required=False
                                         )
    cata_intensidad = MultiSelectFormField(label="Intensidad",
                                           widget=Select2Multiple(select2attrs={'width': '250px'}),
                                           choices=CATA_INTENSIDAD,
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
    cata_olf_1a = MultiSelectFormField(label="1ª impresión",
                                       widget=Select2Multiple(select2attrs={'width': '250px'}),
                                       choices=CATA_OLFATIVA_1IMPRESION,
                                       required=False
                                       )
    cata_olf_intensidad = MultiSelectFormField(label="Intensidad",
                                               widget=Select2Multiple(select2attrs={'width': '250px'}),
                                               choices=CATA_OLFATIVA_INTENSIDAD,
                                               required=False
                                               )
    cata_olf_aroma_1 = MultiSelectFormField(label="Aroma (Carácter) Primarios (cepa)",
                                            widget=Select2Multiple(select2attrs={'width': '250px'}),
                                            choices=CATA_OLFATIVA_AROMA_PRIMARIOS,
                                            required=False
                                            )
    cata_olf_aroma_2 = MultiSelectFormField(label="Aroma (Carácter) Secundarios (fermentación)",
                                            widget=Select2Multiple(select2attrs={'width': '250px'}),
                                            choices=CATA_OLFATIVA_AROMA_SECUNDARIOS,
                                            required=False
                                            )
    cata_olf_aroma_3 = MultiSelectFormField(label="Aroma (Carácter) Terciarios (maduración)",
                                            widget=Select2Multiple(select2attrs={'width': '250px'}),
                                            choices=CATA_OLFATIVA_AROMA_TERCIARIOS,
                                            required=False
                                            )
    cata_gust_ataque = MultiSelectFormField(label="Ataque",
                                            widget=Select2Multiple(select2attrs={'width': '250px'}),
                                            choices=CATA_GUSTATIVA_ATAQUE,
                                            required=False
                                            )
    cata_gust_dulzor = MultiSelectFormField(label="Dulzor",
                                            widget=Select2Multiple(select2attrs={'width': '250px'}),
                                            choices=CATA_GUSTATIVA_DULZOR,
                                            required=False
                                            )
    cata_gust_alcohol = MultiSelectFormField(label="Alcohol",
                                             widget=Select2Multiple(select2attrs={'width': '250px'}),
                                             choices=CATA_GUSTATIVA_ALCOHOL,
                                             required=False
                                             )
    cata_gust_acidez = MultiSelectFormField(label="Acidez",
                                            widget=Select2Multiple(select2attrs={'width': '250px'}),
                                            choices=CATA_GUSTATIVA_ACIDEZ,
                                            required=False
                                            )
    cata_gust_tanino = MultiSelectFormField(label="Tanino",
                                            widget=Select2Multiple(select2attrs={'width': '250px'}),
                                            choices=CATA_GUSTATIVA_TANINO,
                                            required=False
                                            )
    cata_gust_cuerpo = MultiSelectFormField(label="Cuerpo",
                                            widget=Select2Multiple(select2attrs={'width': '250px'}),
                                            choices=CATA_GUSTATIVA_CUERPO,
                                            required=False
                                            )
    cata_gust_boca = MultiSelectFormField(label="Paso en boca",
                                          widget=Select2Multiple(select2attrs={'width': '250px'}),
                                          choices=CATA_GUSTATIVA_BOCA,
                                          required=False
                                          )
    cata_gust_persistencia = MultiSelectFormField(label="Persistencia",
                                                  widget=Select2Multiple(select2attrs={'width': '250px'}),
                                                  choices=CATA_GUSTATIVA_PERSISTENCIA,
                                                  required=False
                                                  )

    class Meta:
        model = Wine
        fields = "__all__"
