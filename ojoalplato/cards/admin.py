from django import forms
from django.forms import widgets
from django.contrib import admin
from django.contrib.gis.geos import Point
from geopy import GoogleV3
from reversion.admin import VersionAdmin

from .widgets import WeekdayWidget, StarsWidget, PointWidget, PhoneNumberWidget
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
            'price': widgets.TextInput(attrs={'style': 'width:100px;', 'placeholder': '€ sin vino'}),
            'avg_price': widgets.NumberInput(attrs={'style': 'width:100px;', 'placeholder': '€ medio'}),
            'menu_price': widgets.NumberInput(attrs={'style': 'width:100px;', 'placeholder': '€ menu'}),
        }
        fields = '__all__'

    def clean(self):
        cleaned_data = super(RestaurantAdminForm, self).clean()
        address = cleaned_data.get("address")
        location = cleaned_data.get("location")

        if address and self.instance.address != address:
            if location == self.instance.location:
                geolocator = GoogleV3()
                location = geolocator.geocode(address)
                if location:
                    point = Point((location.longitude, location.latitude), srid=DEFAULT_WGS84_SRID)
                    cleaned_data["location"] = point

        # Always return the full collection of cleaned data.
        return cleaned_data


@admin.register(Restaurant)
class RestaurantAdmin(VersionAdmin):
    form = RestaurantAdminForm
    list_filter = ['stars', 'is_closed']
    list_display = ['name', 'is_closed']
    save_on_top = True

    class Meta:
        css = {
            'all': ('https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css',),
        }


@admin.register(Wine)
class WineAdmin(VersionAdmin):
    list_filter = ['kind']
    list_display = ['name', 'kind']
    save_on_top = True


@admin.register(Recipe)
class RecipeAdmin(VersionAdmin):
    list_display = ['name']
    save_on_top = True
