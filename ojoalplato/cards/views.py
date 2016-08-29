from django.views.generic import ListView

from ojoalplato.cards.models import Restaurant


class MapView(ListView):
    model = Restaurant
    template_name = "blog/wpfamily/map_list.html"
