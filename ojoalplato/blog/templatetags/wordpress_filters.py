# coding=utf-8
import re

from django import template
from django.utils.encoding import force_text
from django.utils.text import normalize_newlines
from wordpress.models import Post, PostMeta

register = template.Library()


@register.filter()
def dropcap(value):
    value = normalize_newlines(force_text(value))
    paras = re.split('\n{2,}', value)
    first, paras = paras[0], paras[1:]
    first = ['<p class="dropcap-first">%s</p>' % first.replace('\n', '<br />')]
    paras = ['<p>%s</p>' % p.replace('\n', '<br />') for p in paras]
    paras = first + paras
    return '\n\n'.join(paras)


@register.filter()
def views(post):
    try:
        return PostMeta.objects.get(post=post, key="views").value
    except:
        return 0
