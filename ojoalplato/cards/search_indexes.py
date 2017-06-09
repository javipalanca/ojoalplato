import datetime
from haystack import indexes
from .models import Restaurant


class RestaurantIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    chef = indexes.CharField(model_attr='chef')
    location = indexes.LocationField(model_attr="location")

    def get_model(self):
        return Restaurant
