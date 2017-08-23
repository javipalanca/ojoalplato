from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from .serializers import RestaurantSerializer
from ojoalplato.cards.models import Restaurant


class RestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    @list_route()
    def opened(self, request):
        restaurants = Restaurant.objects.filter(is_closed=False)
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)
