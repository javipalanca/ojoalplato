from django import forms
from django.contrib import admin
from django.contrib.gis.geos import Point
from django.forms import widgets
from geopy import Nominatim
from geopy.exc import GeocoderQueryError
from reversion.admin import VersionAdmin

from . import DAY_CHOICES, DEFAULT_WGS84_SRID
from .forms import WineForm
from .models import Restaurant, Wine, Recipe, Winery, VarietyTag
from .widgets import WeekdayWidget, StarsWidget, PointWidget, PhoneNumberWidget, SunsWidget


class RestaurantAdminForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        widgets = {
            'location': PointWidget(),
            'freedays': WeekdayWidget(choices=DAY_CHOICES),
            'phone': PhoneNumberWidget(),
            'stars': StarsWidget(),
            'suns': SunsWidget(),
            'price': widgets.TextInput(attrs={'style': 'width:100px;', 'placeholder': '€ sin vino'}),
            'avg_price': widgets.TextInput(attrs={'style': 'width:100px;', 'placeholder': '€ medio'}),
            'menu_price': widgets.TextInput(attrs={'style': 'width:100px;', 'placeholder': '€ menu'}),
        }
        fields = '__all__'

    def reverse_location(self, address):
        geolocator = Nominatim(user_agent="myGeocoder")  ##GoogleV3()
        try:
            location = geolocator.geocode(address, timeout=20)
        except GeocoderQueryError:
            location = None

        if location:
            point = Point((location.longitude, location.latitude), srid=DEFAULT_WGS84_SRID)
        else:
            point = Point((0, 0), srid=DEFAULT_WGS84_SRID)
        return point

    def clean(self):
        cleaned_data = super(RestaurantAdminForm, self).clean()
        address = cleaned_data.get("address")
        location = cleaned_data.get("location")

        if address and self.instance.address != address:
            if not location or location == self.instance.location:
                cleaned_data["location"] = self.reverse_location(address)
        elif not location:
            cleaned_data["location"] = self.reverse_location(address)

        # Always return the full collection of cleaned data.
        return cleaned_data


@admin.register(Restaurant)
class RestaurantAdmin(VersionAdmin):
    form = RestaurantAdminForm
    search_fields = ("name",)
    list_filter = ['stars', 'is_closed']
    list_display = ['name', 'is_closed']
    save_on_top = True

    fields = ("name", "chef", "sumiller", "manager", "tags", "image_header", "address", "location", "phone",
              "url", "email", "last_visit", "price", "avg_price", "menu_price",
              "stars", "suns", "awards", "freedays", "is_closed", "notes")

    class Media:
        css = {
            'all': ('https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css',
                    'wpfamily/style_admin.css'),
        }
        js = (
            'admin/js/jquery.init.alt.js',
        )


@admin.register(Winery)
class WineryAdmin(VersionAdmin):
    pass


@admin.register(VarietyTag)
class VarietyTagAdmin(VersionAdmin):
    pass


@admin.register(Wine)
class WineAdmin(VersionAdmin):
    search_fields = ("name", "year", "kind")
    list_filter = ['year']
    list_display = ['name', 'year']
    save_on_top = True
    form = WineForm

    fieldsets = (
        (None, {
            "fields": ["name", "winery", "year", "kind", "image_header",
                       "image_bottle", "image_back", "country", "region",
                       "tags", "preparation", "last_taste", "price",
                       "parker_points", "penyin_points", "other",
                       "opinion", "show_tasting_form"]
        }),
        ("Ficha de Cata - Visual", {
            "fields": ["cata_aspecto", "cata_capa",
                       "cata_color_blanco", "cata_color_tinto",
                       "cata_color_rosado", "cata_ribete", "cata_fluidez",
                       "cata_efervescencia"]
        }),
        ("Ficha de Cata - Olfativa", {
            "fields": ["cata_olf_intensidad", "cata_olf_aroma"]
        }),
        ("Ficha de Cata - Gustativa", {
            "fields": ["cata_gust_ataque", "cata_gust_sensacion",
                       "cata_gust_persistencia", "cata_gust_valoracion"]
        })

    )

    class Media:
        css = {
            'all': ('https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css',
                    'wpfamily/style_admin.css'),
        }
        js = (
            'admin/js/jquery.init.alt.js',
        )


@admin.register(Recipe)
class RecipeAdmin(VersionAdmin):
    search_fields = ("name",)
    list_display = ['name']
    save_on_top = True
