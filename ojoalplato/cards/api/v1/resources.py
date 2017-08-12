from rest_framework import viewsets

from .serializers import RestaurantSerializer
from ojoalplato.cards.models import Restaurant


class RestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
