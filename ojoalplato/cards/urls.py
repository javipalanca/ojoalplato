from django.urls import path

from .views import MapView, RestaurantDetailView, WineDetailView, restaurant_search, autocomplete

urlpatterns = [
    path('map/', MapView.as_view(), name='map-list'),
    path('restaurant/<slug:slug>/', RestaurantDetailView.as_view(), name='restaurant-detail'),
    path('wine/<slug:slug>/', WineDetailView.as_view(), name='wine-detail'),
    path('search/', restaurant_search, name='restaurant-search'),
    path('search/autocomplete', autocomplete, name='autocomplete-search'),
]
