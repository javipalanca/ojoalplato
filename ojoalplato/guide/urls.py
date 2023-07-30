from django.conf.urls import url

from .views import GuideDetailView

urlpatterns = [
    url(r'^(?P<slug>[-\w]+)/$', GuideDetailView.as_view(), name='guide-detail'),
]
