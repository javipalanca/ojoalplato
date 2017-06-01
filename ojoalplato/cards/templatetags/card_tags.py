# -*- coding: utf-8 -*-
from copy import copy
from django import template
from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.conf import settings
from django.http import QueryDict

register = template.Library()

from ojoalplato.cards import DEFAULT_PROJECTED_SRID, DEFAULT_GOOGLE_MAPS_SRID


@register.inclusion_tag('cards/templatetags/restaurant.html', takes_context=True)
def render_restaurant_mini(context, restaurant):
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
    #google_maps_point = make_point(point, origin_coord_srid=point.srid, destiny_coord_srid=DEFAULT_GOOGLE_MAPS_SRID)
    base_uri = "https://maps.googleapis.com/maps/api/staticmap"
    args = {
        "maptype": "roadmap",
        "zoom": zoom,
        "size": "{}x{}".format(width, height),
        "key": settings.GOOGLE_MAPS_API_KEY,
        "center": "{},{}".format(point[0], point[1]),
        "markers": "color:red|{},{}".format(point[0], point[1]),
    }
    query_dict = QueryDict(mutable=True)
    query_dict.update(args)
    return "{}?{}".format(base_uri, query_dict.urlencode())


#@register.filter
#def point_google_maps(origin_point):
#    if isinstance(origin_point, Point) and origin_point.srid == DEFAULT_PROJECTED_SRID:
#        point = make_point(
#            origin_point, origin_coord_srid=DEFAULT_PROJECTED_SRID, destiny_coord_srid=DEFAULT_GOOGLE_MAPS_SRID
#        )
#        return "POINT ({} {})".format(point.coords[0], point.coords[1])
#    return origin_point
