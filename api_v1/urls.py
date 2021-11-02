from django.urls import path, include
from rest_framework import routers
from api_v1.views import DishesViewSet

router = routers.DefaultRouter()
# router.register('dishes', DishesViewSet, basename='dishes')

urlpatterns = [
    path('', include(router.urls)),
    path('dishes/get_dishes/', DishesViewSet.as_view({'get': 'get'})),
]