from django import template

register = template.Library()


@register.inclusion_tag('guide/templatetags/restaurant.html', takes_context=True)
def render_restaurant_full(context, restaurant):
    """Renders a restaurant mini card."""
    request = context["request"]
    context["restaurant"] = restaurant
    return context
