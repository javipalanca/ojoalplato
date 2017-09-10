from django import forms
from django.forms import widgets
from django.contrib import admin
from django.contrib.gis.geos import Point
from geopy import GoogleV3
from geopy.exc import GeocoderQueryError
from reversion.admin import VersionAdmin

from .widgets import WeekdayWidget, StarsWidget, PointWidget, PhoneNumberWidget, SunsWidget
from . import DAY_CHOICES, DEFAULT_WGS84_SRID
from .models import Restaurant, Wine, Recipe


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
        geolocator = GoogleV3()
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
    search_fields = ("name", )
    list_filter = ['stars', 'is_closed']
    list_display = ['name', 'is_closed']
    save_on_top = True

    fields = ("name", "chef", "tags", "image_header", "address", "location", "phone", "url", "email",
              "last_visit", "price", "avg_price", "menu_price",
              "stars", "suns", "awards", "freedays", "is_closed", "notes")

    class Meta:
        css = {
            'all': ('https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css',
                    'wpfamily/style_admin.css'),
        }


@admin.register(Wine)
class WineAdmin(VersionAdmin):
    search_fields = ("name",)
    list_filter = ['kind']
    list_display = ['name', 'kind']
    save_on_top = True


@admin.register(Recipe)
class RecipeAdmin(VersionAdmin):
    search_fields = ("name",)
    list_display = ['name']
    save_on_top = True
