from django import template

register = template.Library()


@register.inclusion_tag('signature.html', takes_context=False)
def signature(post):
    if 'ojoalplato.blog' in post.content:
        return {"signature": ""}
    else:
        m = """<span style="font-size: 10px;">Fotografías: © Paco Palanca /&nbsp;Instagram: @ojoalplato.blog&nbsp; /&nbsp;Facebook: @ojoalplato /Twitter: @ojoalplato /Twitter: @pacopalanca</span><br>"""
        return {"signature": m}
