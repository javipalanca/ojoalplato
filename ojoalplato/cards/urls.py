from django.conf.urls import url

from .views import MapView, RestaurantDetailView

urlpatterns = [
    url(r'^map/$', MapView.as_view(), name='map-list'),
    url(r'^restaurant/(?P<slug>[-\w]+)/$', RestaurantDetailView.as_view(), name='restaurant-detail'),
]
