# -*- coding: utf-8 -*-
from copy import copy

from django import template
from django.conf import settings
from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.http import QueryDict
from django.utils.safestring import mark_safe
from six import string_types

from ojoalplato.cards.widgets import sun_set, star_set_2

register = template.Library()

from .. import WINE_KIND_CHOICES, RED_ICON, WHITE_ICON, ROSE_ICON, \
    SWEET_ICON, SPARKS_ICON


@register.inclusion_tag('cards/templatetags/restaurant.html', takes_context=True)
def render_restaurant_mini(context, restaurant):
    """Renders a restaurant mini card."""
    request = context["request"]
    context["restaurant"] = restaurant
    return context


@register.inclusion_tag('cards/templatetags/restaurant_full.html', takes_context=True)
def render_restaurant(context, restaurant):
    """Renders a restaurant mini card."""
    request = context["request"]
    context["restaurant"] = restaurant
    return context


def make_point(point, origin_coord_srid, destiny_coord_srid):
    origin_coord = SpatialReference(origin_coord_srid)
    destination_coord = SpatialReference(destiny_coord_srid)
    trans = CoordTransform(origin_coord, destination_coord)
    transformed_point = copy(point)
    transformed_point.transform(trans)
    return transformed_point


@register.simple_tag
def google_static_map(point, width=600, height=300, zoom=10):
    base_uri = "https://maps.googleapis.com/maps/api/staticmap"
    args = {
        "maptype": "roadmap",
        "zoom": zoom,
        "size": "{}x{}".format(width, height),
        "key": settings.GOOGLE_MAPS_API_KEY,
        "center": "{},{}".format(point[1], point[0]),
        "markers": "color:red|{},{}".format(point[1], point[0]),
    }
    query_dict = QueryDict(mutable=True)
    query_dict.update(args)
    return "{}?{}".format(base_uri, query_dict.urlencode())


@register.filter
def card_bs_suns_fa(num, max_stars=5):
    """
    Suns for Font Awesome w icon-sun
    If num is not None, the returned string will contain num solid suns
    followed by max_stars - num empty stars
    """
    return mark_safe(render_stars(num, max_stars, sun_set, "suns"))


@register.filter
def card_bs_stars3(num, max_stars=5):
    """
    Stars for Bootstrap 3

    If num is not None, the returned string will contain num solid stars
    followed by max_stars - num empty stars
    """
    return mark_safe(render_stars(num, max_stars, star_set_2, "stars"))


def render_stars(num, max_stars, star_set, name):
    """
    Star renderer returns a HTML string of stars
    If num is None or a blank string, it returns the unanswered tag
    Otherwise, the returned string will contain num solid stars
    followed by max_stars - num empty stars
    If num > max_stars, render max_stars solid stars
    star_set is a dictionary of strings with keys: star, unlit, noanswer
    """
    if num is None or (isinstance(num, string_types) and len(num) == 0):
        return '<span>' + star_set['noanswer'] + '</span>'

    difference = int(max_stars) - int(num)
    if difference < 0:
        num = max_stars
        difference = 0

    stars = ''.join(star_set['star'] * int(num) + star_set['unlit'] * difference)
    return '<span>' + stars + '</span>'


@register.filter(name='get_class')
def get_class(value):
    return value.__class__.__name__


@register.filter
def decode_kind(kinds):
    """
    Decode wine kinds
    """
    decoder = dict(WINE_KIND_CHOICES)
    decoded = [decoder[k] for k in kinds]
    return decoded


@register.filter
def get_wine_icons(text):
    icons = {"Tinto": RED_ICON,
             "Blanco": WHITE_ICON,
             "Rosado": ROSE_ICON,
             "Dulce": SWEET_ICON,
             "Espumoso": SPARKS_ICON}
    result = ""
    for kind in text.split(","):
        try:
            icon = icons[kind.strip()]
        except KeyError:
            icon = ""

        result += f"<span>{icon}&nbsp;{kind}</span>&nbsp;"
    return result


@register.filter
def parker_points(points):
    return scale_points(points, "bg-danger progress-bar-danger")


@register.filter
def penyin_points(points):
    return scale_points(points, "bg-success progress-bar-success")


def scale_points(points, color):
    return f"""<div class="progress-bar progress-bar-striped {color}" role="progressbar"
     aria-label="{points} Points" style="width: {points}%" aria-valuenow="{points}"
     aria-valuemin="0" aria-valuemax="100">{points}</div>"""


@register.inclusion_tag('cards/templatetags/tasting_form.html', takes_context=True)
def render_tasting_form(context, wine):
    """Renders a restaurant mini card."""
    request = context["request"]
    context["wine"] = wine
    return context


@register.inclusion_tag('cards/templatetags/wine.html', takes_context=True)
def render_wine_mini(context, wine):
    """Renders a restaurant mini card."""
    request = context["request"]
    context["wine"] = wine
    return context


@register.filter
def as_comma_list(tags):
    return ", ".join([t.name for t in tags.all()])
