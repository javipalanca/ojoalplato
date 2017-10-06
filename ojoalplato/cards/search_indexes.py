from haystack import indexes
from .models import Restaurant


class RestaurantIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr="name", null=False)
    chef = indexes.CharField(model_attr='chef', null=True)
    address = indexes.CharField(model_attr="address", null=True)
    img_src = indexes.CharField(model_attr="img_src", null=True)
    absolute_url = indexes.CharField(model_attr="absolute_url", null=True)
    stars = indexes.IntegerField(model_attr="stars", null=True)
    suns = indexes.IntegerField(model_attr="suns", null=True)
    awards = indexes.CharField(model_attr="awards", null=True)
    is_closed = indexes.BooleanField(model_attr="is_closed", null=True)
    last_visit = indexes.DateTimeField(model_attr='last_visit', null=True)
    location = indexes.LocationField(model_attr="location_wgs84_reverse", null=True)

    # We add this for autocomplete.
    content_auto = indexes.EdgeNgramField(model_attr='autocomplete_text')

    def get_model(self):
        return Restaurant
