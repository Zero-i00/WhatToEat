from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from .views import IndexView
from .views import IndexView, ThreeDishesView


urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('three_random_dishes', ThreeDishesView.as_view(), name="three_random_dishes"),
]
