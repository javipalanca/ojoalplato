from django.conf.urls import url

from .views import MapView, RestaurantDetailView, restaurant_search, autocomplete

urlpatterns = [
    url(r'^map/$', MapView.as_view(), name='map-list'),
    url(r'^restaurant/(?P<slug>[-\w]+)/$', RestaurantDetailView.as_view(), name='restaurant-detail'),
    url(r'^search/$', restaurant_search, name='restaurant-search'),
    url(r'^search/autocomplete$', autocomplete, name='autocomplete-search'),
]
