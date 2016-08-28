import pickle
from django.contrib.gis.geos import Point
from django.core.management import BaseCommand
from geopy import Nominatim

from ojoalplato.cards import DEFAULT_WGS84_SRID
from ojoalplato.cards.models import Restaurant


class Command(BaseCommand):
    help = 'Import restaurants from google maps kml'

    def handle(self, *args, **options):
        f = open("restaurants.pickle", 'rb')
        d = pickle.load(f)

        for name, v in d.items():
            if name.startswith("Restaurante "):
                name = name[len("Restaurante "):].strip()
            r = Restaurant(name=name)
            position_point = Point(v['x'], v['y'], srid=DEFAULT_WGS84_SRID)
            location = position_point
            if 'post_id' in v:
                r.notes = v["post_id"]

            geolocator = Nominatim()
            x, y = location.x, location.y
            reverse_location = geolocator.reverse("{0}, {1}".format(y, x))
            r.address = reverse_location.address
            r.save()
            r.location = location
            r.save()
