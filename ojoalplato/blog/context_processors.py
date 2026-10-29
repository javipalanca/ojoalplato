from django.core.cache import cache

from ojoalplato.blog.models import SiteSettings, MenuItem, CircleCategory

MENU_CACHE_KEY = "site_menu_items"
CIRCLES_CACHE_KEY = "site_circle_categories"
CACHE_TIMEOUT = 60 * 60  # 1 hora


def _menu_items():
    items = cache.get(MENU_CACHE_KEY)
    if items is None:
        items = list(MenuItem.objects.filter(active=True))
        cache.set(MENU_CACHE_KEY, items, CACHE_TIMEOUT)
    return items


def _circle_categories():
    circles = cache.get(CIRCLES_CACHE_KEY)
    if circles is None:
        circles = list(CircleCategory.objects.filter(active=True))
        cache.set(CIRCLES_CACHE_KEY, circles, CACHE_TIMEOUT)
    return circles


def site_settings(request):
    return {
        "site_settings": SiteSettings.load(),
        "menu_items": _menu_items(),
        "circle_categories": _circle_categories(),
    }
