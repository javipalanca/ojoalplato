from django.views.generic import DetailView, ListView

from ojoalplato.cards.models import Restaurant

from haystack.forms import HighlightedModelSearchForm
from haystack.generic_views import SearchView


class MapView(SearchView):
    model = Restaurant
    template_name = "blog/wpfamily/map_list.html"
    form = HighlightedModelSearchForm


class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = "cards/restaurant_detail.html"
    context_object_name = "card"
