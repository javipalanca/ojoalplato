from django import template

register = template.Library()


@register.inclusion_tag('signature.html', takes_context=False)
def signature(post):
    try:
        has_signature = 'ojoalplato.blog' in post.content
        ret =  {"signature": ""}
    except AttributeError:
        m = """<span style="font-size: 10px;">Fotografías: © Paco Palanca /&nbsp;Instagram: @ojoalplato.blog&nbsp; /&nbsp;Facebook: @ojoalplato /Twitter: @ojoalplato /Twitter: @pacopalanca</span><br>"""
        ret = {"signature": m}
    return ret
