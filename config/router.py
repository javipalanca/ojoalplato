# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter

from ojoalplato.cards.api.v1.resources import RestaurantViewSet

router = SimpleRouter()

router.register(r'restaurants', viewset=RestaurantViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
