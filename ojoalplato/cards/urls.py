from django.urls import path, re_path

from .views import MapView, RestaurantDetailView, WineDetailView, restaurant_search, autocomplete

urlpatterns = [
    path('map/', MapView.as_view(), name='map-list'),
    re_path(r'^restaurant/(?P<slug>[-\w]+)/$', RestaurantDetailView.as_view(), name='restaurant-detail'),
    re_path(r'^wine/(?P<slug>[-\w]+)/$', WineDetailView.as_view(), name='wine-detail'),
    path('search/', restaurant_search, name='restaurant-search'),
    path('search/autocomplete', autocomplete, name='autocomplete-search'),
]
