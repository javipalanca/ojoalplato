from django.contrib import admin
from reversion.admin import VersionAdmin

from ojoalplato.guide.models import Guide


@admin.register(Guide)
class GuideAdmin(VersionAdmin):
    search_fields = ("title", "city")
    list_filter = ['city']
    list_display = ['city', 'title']
    filter_horizontal = ('restaurants',)
    save_on_top = True
