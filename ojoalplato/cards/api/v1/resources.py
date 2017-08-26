from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from drf_haystack.filters import HaystackAutocompleteFilter
from drf_haystack.viewsets import HaystackViewSet
from rest_framework.permissions import AllowAny

from .serializers import RestaurantSerializer, RestaurantAutocompleteSerializer
from ojoalplato.cards.models import Restaurant


class RestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    @list_route()
    def opened(self, request):
        restaurants = Restaurant.objects.filter(is_closed=False)
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)


class AutocompleteRestaurantSearchViewSet(HaystackViewSet):

    index_models = [Restaurant]
    serializer_class = RestaurantAutocompleteSerializer
    filter_backends = [HaystackAutocompleteFilter]
    permission_classes = [AllowAny]
