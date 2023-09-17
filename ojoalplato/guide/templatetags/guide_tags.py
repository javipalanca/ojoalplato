from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.inclusion_tag('guide/templatetags/restaurant.html', takes_context=True)
def guide_render_restaurant_full(context, restaurant):
    """Renders a restaurant mini card."""
    request = context["request"]
    context["restaurant"] = restaurant
    return context


@register.filter
def parse_float_to_str(num):
    return str(num).replace(',', '.')
