from django import template

register = template.Library()


@register.inclusion_tag('facebook_js.html', takes_context=False)
def facebook_js():
    return {}


@register.inclusion_tag('fb_like.html', takes_context=False)
def fb_like_button(post):
    return {"post": post}
