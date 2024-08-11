from django.urls import re_path

from .views import GuideDetailView

urlpatterns = [
    re_path(r'^(?P<slug>[-\w]+)/$', GuideDetailView.as_view(), name='guide-detail'),
]
