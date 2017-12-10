# coding=utf-8
import urllib
import re
from uuid import uuid4

from django.utils.safestring import mark_safe
from io import BytesIO

from PIL import Image
from bs4 import BeautifulSoup

from django.conf import settings
from django import template
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.encoding import force_text
from django.utils.text import normalize_newlines, slugify

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
        from ojoalplato.blog.models import PostMeta
        return PostMeta.objects.get(post=post, key="views").value
    except:
        return 0


@register.filter()
def lightbox(post):
    soup = BeautifulSoup(post, "html.parser")
    for img in soup.findAll('img'):
        img["src"] = media(img["src"])
        src = media(img.attrs["src"])
        if "alt" in img.attrs:
            alt = slugify(img.attrs["alt"])
        else:
            alt = uuid4()
        a = soup.new_tag("a", **{"href": src, "data-lightbox": alt, "alt": alt, "class": "image-link"})  # create an A element
        img.replaceWith(a)  # Put it where the IMG element is
        if "style" in img.attrs:
            img.attrs["style"] += ' border-radius:4px;'
        else:
            img.attrs["style"] = ' border-radius:4px;'
        a.insert(0, img)  # Put the IMG element inside the A (between <a> and </a>)

    return str(soup)


@register.filter()
def first_img(post):
    soup = BeautifulSoup(post, "html.parser")
    img = soup.find('img')
    if img:
        return img.attrs["src"]
    else:
        return settings.STATIC_URL + "wpfamily/img/logo2.png"


@register.filter()
def relative_url(url):
    return url


@register.filter()
def media(url):
    AWS_PATH = "https://ojoalplato-static.s3.amazonaws.com"
    if url:
       if url.startswith("/media"):
            return AWS_PATH + url
    url = url.replace("//media", "/media")
    return url


@register.filter()
def cat_img(category):
    images = {
        "restaurantes": "cuberteria.jpg",
        "vinos": "wine.jpg",
        "recetas": "recipe.jpg",
        "cervezas": "beer.jpg",
        "cigarros": "cigars.jpg",
        "comentarios-propios": "microphone.jpg",
    }
    if category.lower() in images:
        return images[category.lower()]
    else:
        return "uncategorized.gif"


@register.simple_tag(takes_context=True)
def active(context, pattern_or_urlname):
    try:
        pattern = '^' + reverse(pattern_or_urlname)
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path):
        return 'current-menu-item'
    return ''


@register.simple_tag(takes_context=True)
def og_img_size(context, url):
    try:
        if not url.startswith("http"):
            domain = context["request"].get_host()
            url = "http://{}{}".format(domain, url)
        file = BytesIO(urllib.request.urlopen(url).read())
        img = Image.open(file)
        w, h = img.size
    except:
        w, h = 100, 100
    meta = '<meta property="og:image:width" content="{}"><meta property="og:image:height" content="{}">'.format(w, h)
    return mark_safe(meta)


@register.filter
def escape_slash(value):
    return value.replace("/", "\/")
