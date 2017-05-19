# -*- coding: utf-8 -*-
from django import template

register = template.Library()

from ojoalplato.cards import DEFAULT_PROJECTED_SRID, DEFAULT_GOOGLE_MAPS_SRID


@register.inclusion_tag('cards/templatetags/restaurant.html', takes_context=True)
def render_restaurant_mini(context, restaurant):
    """Renders a restaurant mini card."""
    request = context["request"]
    context["restaurant"] = restaurant
    return context


@register.filter
def point_google_maps(origin_point):
    if isinstance(origin_point, Point) and origin_point.srid == DEFAULT_PROJECTED_SRID:
        point = make_point(
            origin_point, origin_coord_srid=DEFAULT_PROJECTED_SRID, destiny_coord_srid=DEFAULT_GOOGLE_MAPS_SRID
        )
        return "POINT ({} {})".format(point.coords[0], point.coords[1])
    return origin_point
