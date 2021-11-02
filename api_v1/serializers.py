from rest_framework import serializers
from core.models import *


class DishesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dishes
        fields = ('__all__')
        depth = 1