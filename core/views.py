from django.db.models import Q
from django.shortcuts import render
from django.views import View
from core.models import *
from random import choice

class IndexView(View):
    template_name = 'core/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

def get_dishes():

    main_dishes = choice(Dishes.objects.filter(dish_type='main'))
    soups = choice(Dishes.objects.filter(dish_type='soup'))
    salads = choice(Dishes.objects.filter(dish_type='salad'))

    return Dishes.objects.filter(Q(id=main_dishes.id) | Q(id=soups.id) | Q(id=salads.id))

class ThreeDishesView(View):
    template_name = 'core/three_dishes_index.html'

    def get(self, request):
        dishes = get_dishes()
        return render(request, self.template_name, {
            'dishes': dishes,
        })

    def post(self, request):
        dishes = get_dishes()
        return render(request, self.template_name, {
            'dishes': dishes,
        })