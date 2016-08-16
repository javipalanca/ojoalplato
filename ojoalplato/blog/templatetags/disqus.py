from django import template

register = template.Library()


@register.inclusion_tag('disqus_comments.html', takes_context=False)
def disqus_comments(post):
    return {"post": post}
