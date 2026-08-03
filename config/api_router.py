from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from ojoalplato.blog.api.v1.resources import AutocompletePostSearchViewSet
from ojoalplato.cards.api.v1.resources import RestaurantViewSet, AutocompleteRestaurantSearchViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register(r'restaurants', viewset=RestaurantViewSet)
router.register("posts/search/autocomplete", viewset=AutocompletePostSearchViewSet,
                basename="post-search-autocomplete")
router.register("restaurants/search/autocomplete", viewset=AutocompleteRestaurantSearchViewSet,
                basename="restaurant-search-autocomplete")


app_name = "api"
urlpatterns = router.urls
