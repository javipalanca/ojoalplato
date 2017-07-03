from haystack import indexes
from .models import Restaurant


class RestaurantIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    chef = indexes.CharField(model_attr='chef')
    last_visit = indexes.DateTimeField(model_attr='last_visit')

    def get_model(self):
        return Restaurant
