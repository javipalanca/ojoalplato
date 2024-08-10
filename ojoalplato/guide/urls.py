from django.urls import path

from .views import GuideDetailView

urlpatterns = [
    path('<slug:slug>/', GuideDetailView.as_view(), name='guide-detail'),
]
