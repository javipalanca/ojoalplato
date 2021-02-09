# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter

from ojoalplato.blog.api.v1.resources import AutocompletePostSearchViewSet
from ojoalplato.cards.api.v1.resources import RestaurantViewSet, AutocompleteRestaurantSearchViewSet

router = SimpleRouter()

router.register(r'restaurants', viewset=RestaurantViewSet)
router.register("posts/search/autocomplete", viewset=AutocompletePostSearchViewSet,
                basename="post-search-autocomplete")
router.register("restaurants/search/autocomplete", viewset=AutocompleteRestaurantSearchViewSet,
                basename="restaurant-search-autocomplete")


urlpatterns = [
    url(r'^', include(router.urls)),
]
