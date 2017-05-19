from django.views.generic import ListView, DetailView

from ojoalplato.cards.models import Restaurant


class MapView(ListView):
    model = Restaurant
    template_name = "blog/wpfamily/map_list.html"


class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = "cards/card_detail.html"
    context_object_name = "card"
