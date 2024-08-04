from django import template

register = template.Library()


@register.inclusion_tag('signature.html', takes_context=False)
def signature(post):
    m = """<span style="font-size: 10px;">Fotografías: © Paco Palanca /&nbsp;Instagram: @ojoalplato.blog&nbsp; /&nbsp;Facebook: @ojoalplato /Twitter: @ojoalplato /Twitter: @pacopalanca</span><br>"""
    try:
        has_signature = '@pacopalanca' in post.content
        if has_signature:
            m = ""
    except AttributeError:
        pass
    ret = {"signature": m}
    return ret
