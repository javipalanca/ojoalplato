from rest_framework import serializers
from rest_framework_gis.fields import GeometryField
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer

from drf_haystack.serializers import HaystackSerializer

from ojoalplato.cards.models import Restaurant
from ojoalplato.cards.search_indexes import RestaurantIndex


class RestaurantSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    location = GeometryField(source="location_wgs84")

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'slug', 'chef', 'address', 'phone', 'url', 'email',
                  'last_visit', 'price', 'avg_price', 'menu_price', 'location',
                  'stars', 'suns', 'awards', 'freedays', 'is_closed', 'tags')


class RestaurantAutocompleteSerializer(HaystackSerializer):

    class Meta:
        index_classes = [RestaurantIndex]
        fields = ["name", "chef", "address", "img_src", "absolute_url",
                  "stars", "suns", "location", "is_closed", "content_auto"]
        ignore_fields = ["content_auto"]

        # The `field_aliases` attribute can be used in order to alias a
        # query parameter to a field attribute. In this case a query like
        # /search/?q=oslo would alias the `q` parameter to the `autocomplete`
        # field on the index.
        field_aliases = {
            "q": "content_auto"
        }
