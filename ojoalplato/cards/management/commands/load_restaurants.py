import json
from django.contrib.gis.geos import Point
from django.core.management import BaseCommand
from tqdm import tqdm
from geopy import Nominatim
from geopy import GoogleV3

from ojoalplato.blog.models import Post
from ojoalplato.cards import DEFAULT_WGS84_SRID
from ojoalplato.cards.models import Restaurant


class Command(BaseCommand):
    help = 'Import restaurants from google maps kml'

    def handle(self, *args, **options):
        f = open("restaurant.json", 'r')
        d = json.load(f)

        for name, v in tqdm(d.items()):
            if name.startswith("Restaurante "):
                name = name[len("Restaurante "):].strip()
            try:
                r = Restaurant.objects.get(name=name)
            except:
                r = Restaurant(name=name)

            r.address = v["address"]
            r.is_closed = v["cerrado"]
            if v["chef"]:
                r.chef = v["chef"].strip()
            if v["notes"]:
                r.notes = v["notes"]
            if v["phone"]:
                r.phone = "+34" + v["phone"]
            if v["email"]:
                r.email = v["email"].strip()
            if v["precio_medio"]:
                r.price = float(v["precio_medio"])
            freedays = {'L': 0, 'M': 1, 'X': 2, 'J': 3, 'V': 4, 'S': 5, 'D': 6}
            if v["cierra"]:
                r.freedays = ",".join([str(freedays[day]) for day in v["cierra"]])

            #if v['x'] and v['y']:
            #    position_point = Point(v['x'], v['y'], srid=DEFAULT_WGS84_SRID)
            #    location = position_point
            #else:
            #    geolocator = GoogleV3(timeout=5)
            #    location = geolocator.geocode(r.address)
            #    if location:
            #        location = Point((location.longitude, location.latitude), srid=DEFAULT_WGS84_SRID)
            #    else:
            #        location = Point((0, 0))

                #geolocator = Nominatim()
                #x, y = location.x, location.y
                #reverse_location = geolocator.reverse("{0}, {1}".format(y, x))
                #r.address = reverse_location.address
                #r.save()
            #r.location = location

            r.save()

            if v["tags"]:
                for tag in v["tags"]:
                    r.tags.add(tag)

            if v['post_id']:
                post_id = v["post_id"]
                for t in post_id.split("<br>"):
                    if "archives/" in t:
                        post_id = t.split("archives/")[1]
                        if "#" in post_id:
                            post_id = post_id.split("#")[0]
                        try:
                            post = Post.objects.get(id=post_id)
                            post.restaurant_card = r
                            post.save()
                        except:
                            pass

            r.save()
