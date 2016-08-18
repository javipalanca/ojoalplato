from django.contrib import admin
from categories import admin as categories_admin
from categories.models import Category as Categories
from categories.admin import CategoryBaseAdmin

from .models import Category

admin.site.unregister(Categories)

@admin.register(Category)
class CategoryAdmin(CategoryBaseAdmin):
    pass
