from django import forms
from django.contrib import admin
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from reversion.admin import VersionAdmin

from .widgets import WeekdayWidget, StarsWidget, PointWidget
from . import DAY_CHOICES
from .models import Restaurant, Wine, Recipe


class RestaurantAdminForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        widgets = {
            'location': PointWidget(),
            'freedays': WeekdayWidget(choices=DAY_CHOICES),
            'phone': PhoneNumberPrefixWidget,
            'stars': StarsWidget(),
        }
        fields = '__all__'


@admin.register(Restaurant)
class RestaurantAdmin(VersionAdmin):
    form = RestaurantAdminForm
    list_filter = ['name', 'price']
    list_display = ['name']

    class Meta:
        css = {
            'all': ('https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css',),
        }


@admin.register(Wine)
class WineAdmin(VersionAdmin):
    list_filter = ['name', 'kind', 'price']
    list_display = ['name', 'kind']


@admin.register(Recipe)
class RecipeAdmin(VersionAdmin):
    list_filter = ['name']
    list_display = ['name']


