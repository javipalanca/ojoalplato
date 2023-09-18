from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_haystack.filters import HaystackAutocompleteFilter
from drf_haystack.viewsets import HaystackViewSet
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, AllowAny
from rest_framework.response import Response

from ojoalplato.cards.models import Restaurant
from .serializers import SimpleRestaurantSerializer, RestaurantAutocompleteSerializer


class RestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Restaurant.objects.all()
    serializer_class = SimpleRestaurantSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    # @method_decorator(cache_page(60 * 60 * 24))
    @action(detail=False)
    def opened(self, request):
        restaurants = Restaurant.objects.filter(is_closed=False)
        serializer = SimpleRestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)


class AutocompleteRestaurantSearchViewSet(HaystackViewSet):

    index_models = [Restaurant]
    serializer_class = RestaurantAutocompleteSerializer
    filter_backends = [HaystackAutocompleteFilter]
    permission_classes = [AllowAny]
