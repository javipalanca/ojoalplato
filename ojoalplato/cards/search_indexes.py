from haystack import indexes
from .models import Restaurant


class RestaurantIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    chef = indexes.CharField(model_attr='chef', null=True)
    last_visit = indexes.DateTimeField(model_attr='last_visit', null=True)
    location = indexes.LocationField(model_attr="location_wgs84", null=True)

    # We add this for autocomplete.
    content_auto = indexes.EdgeNgramField(model_attr='autocomplete_text')

    def get_model(self):
        return Restaurant
