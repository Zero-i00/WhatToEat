from django.shortcuts import render
from rest_framework.views import APIView

from core.models import *
from core.views import get_dishes
from .serializers import *
from rest_framework import viewsets
from rest_framework.response import Response


class DishesViewSet(viewsets.ViewSet):

    def get(self, request):
        queryset_dishes = get_dishes()
        serializer = DishesSerializer(queryset_dishes, many=True)
        return Response(serializer.data)