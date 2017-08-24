from rest_framework import serializers
from rest_framework_gis.fields import GeometryField
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer

from ojoalplato.cards.models import Restaurant


class RestaurantSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    location = GeometryField(source="location_wgs84")

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'slug', 'chef', 'address', 'phone', 'url', 'email',
                  'last_visit', 'price', 'avg_price', 'menu_price', 'location',
                  'stars', 'suns', 'awards', 'freedays', 'is_closed', 'tags')

