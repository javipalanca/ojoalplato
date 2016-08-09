import re
import MySQLdb as mdb
from django.conf import settings

from django.core.management import BaseCommand
from django.utils.text import slugify

from ojoalplato.blog.models import Post


def get_galleries():
    galleries = {}
    con = mdb.connect("mysql", 'ojoalplato', 'ojoalplato', 'wordpress')
    cur = con.cursor()
    cur.execute("SELECT gid,path FROM wordpress.wp_d3r46v_ngg_gallery;")
    for g in cur.fetchall():
        galleries[int(g[0])] = g[1].replace("/wp-content/gallery/", "").replace("wp-content/gallery/", "")

    return galleries


def get_pictures():
    pictures = {}
    con = mdb.connect("mysql", 'ojoalplato', 'ojoalplato', 'wordpress')
    cur = con.cursor()
    cur.execute("SELECT pid,galleryid,filename,description,alttext FROM wordpress.wp_d3r46v_ngg_pictures;")
    for p in cur.fetchall():
        pictures[int(p[0])] = {"galleryid": int(p[1]), "filename": p[2], "description": p[3], "alttext": p[4]}

    return pictures


class Command(BaseCommand):
    help = 'Migrate images from ng-gallery to redactor'

    def handle(self, *args, **options):
        galleries = get_galleries()
        pictures = get_pictures()

        singlepic_re = re.compile(
            "\[singlepic\s*id\s*=\s*(?P<id>\d+)\s*w\s*=\s*(?P<width>\d*)\s*h\s*=\s*(?P<height>\d*)\s*float\s*=\s*(?P<float>left|right|center|none)\s*\]")
        gallery_re = re.compile("\[gallery\s*=\s*(?P<id>\d+)\s*\]")
        align = {"right": "margin: 0px 0px 10px 10px; float: right;",
                 "left": "float: left; margin: 0px 10px 10px 0px;",
                 "center": "margin: auto; display: block;"}
        img = '<p><img data-lightbox="{lightbox}" src="{src}" alt="{alt}" style="width: {width}px; {align}" width="{width}"/></p>'

        for post in Post.objects.filter(status="publish"):
            print(post.title)
            content = post.content
            match = singlepic_re.search(content)
            images = ""
            while match is not None:
                span = match.span()
                subs = content[span[0]:span[1]]
                values = match.groupdict()
                picture = pictures[int(values['id'])]
                gallery = galleries[int(picture["galleryid"])]
                src = settings.MEDIA_URL + "gallery/" + gallery + "/" + picture["filename"]
                if picture["description"]:
                    alt = picture["description"]
                elif picture["alttext"]:
                    alt = picture["alttext"]
                else:
                    alt = ""
                lb = slugify(alt)
                width = str(min(480, int(values["width"])))
                content = content.replace(subs, img.format(src=src, lightbox=lb, alt=alt, width=width,
                                                           align=align[values["float"]]), 1)
                match = singlepic_re.search(content)

            match = gallery_re.search(content)
            while match is not None:
                span = match.span()
                subs = content[span[0]:span[1]]
                galleryid = int(match.groupdict()["id"])
                con = mdb.connect("mysql", 'ojoalplato', 'ojoalplato', 'wordpress')
                cur = con.cursor()
                cur.execute("""SELECT sortorder,filename,description,alttext
                               FROM wordpress.wp_d3r46v_ngg_pictures
                               WHERE galleryid = {gid}
                               ORDER BY sortorder ASC;""".format(gid=galleryid))
                for i in cur.fetchall():
                    gallery = galleries[galleryid]
                    src = settings.MEDIA_URL + "gallery/" + gallery + "/" + i[1]
                    if i[2]:
                        alt = i[2]
                    elif i[3]:
                        alt = i[3]
                    else:
                        alt = ""
                    images += '''<a href="{src}" data-lightbox="{gid}" alt="{alt}" class="image-link">
                                    <img src={src} alt="{alt}" style="width: 7rem; border-radius:4px" width="7rem">
                                </a>'''.format(src=src, gid=galleryid, alt=alt)
                content = content.replace(subs, images)

                match = gallery_re.search(content)

            post.content_filtered = post.content
            post.content = content
            post.save()
