from django.db import models

DISHES_TYPE = (
    ('soup', 'soup'),
    ('salad', 'salad'),
    ('main', 'main'),
)

class Dishes(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='dish/image')
    description = models.CharField(max_length=2500)
    cooking_time = models.IntegerField()
    dish_type = models.CharField(max_length=50, choices=DISHES_TYPE)
    link = models.CharField(max_length=1000)
    ingredients = models.ManyToManyField('Ingredient', related_name='dish_to_ingredient')
    recipes = models.ManyToManyField('Recipe', related_name='dish_to_recipe')


    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title



class Ingredient(models.Model):
    title = models.CharField(max_length=200)
    grammar = models.CharField(max_length=255)


class Recipe(models.Model):
    step_position = models.IntegerField()
    step_text = models.CharField(max_length=2500)

