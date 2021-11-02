from core.models import *
from WhatToEatToday.celery import app
from bs4 import BeautifulSoup
import requests
import re
import json, lxml

@app.task
def create_sources(*args, **kwargs):
    url = 'https://kedem.ru/recipe/'
    HEADERS = {
        'Accept': '*/*',
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    }
    src = requests.get(url, headers=HEADERS).text
    soup = BeautifulSoup(src, 'lxml')  # Главная страница
    all_category_hrefs = soup.find_all('a', class_='menupage')  # Ссылки на категории
    all_category_dict = {}  # Все категории рецептов

    for item_category in all_category_hrefs:
        item_category_text = item_category.text
        if item_category_text == 'Салаты':
            item_category_salads_href = 'https://kedem.ru' + item_category.get('href')
            all_category_dict['salad'] = item_category_salads_href
        elif item_category_text == 'Вторые блюда':
            item_category_MainDish_href = 'https://kedem.ru' + item_category.get('href')
            all_category_dict['main'] = item_category_MainDish_href
        elif item_category_text == 'Супы':
            item_category_soup_href = 'https://kedem.ru' + item_category.get('href')
            all_category_dict['soup'] = item_category_soup_href
        print(item_category.text)

    dishes_dict = {}  # Все рецепты
    for recipes_type, recipes_href in all_category_dict.items():
        src_recipes = requests.get(url=recipes_href, headers=HEADERS).text
        soup_recipes = BeautifulSoup(src_recipes, 'lxml')
        all_dishes = soup_recipes.find_all('a', {'class': 'recipeblocktext'})
        for item_in_recipes in all_dishes:
            item_in_recipes_text = item_in_recipes.text
            item_in_recipes_href = 'https://kedem.ru' + item_in_recipes.get('href')
            dishes_dict[item_in_recipes_text] = {
                'href': item_in_recipes_href,
                'type': recipes_type
            }
    cooking_dict = {}  # Картинка, ингредиенты, готовка блюда
    cooking_ingredients_dict = {}
    cooking_step_by_step_dict = {}
    num = 0
    for type_name, cooking_info in dishes_dict.items():
        try:
            src_cooking = requests.get(url=cooking_info['href'], headers=HEADERS).text
            soup_cooking = BeautifulSoup(src_cooking, 'lxml')
            cooking_page = soup_cooking.find(class_='recipediv')
            cooking_link = cooking_info['href']
            cooking_item_name = cooking_page.find('a', {'class': 'w-lightbox w-inline-block'}).get('title')
            cooking_item_image_link = 'https://kedem.ru' + cooking_page.find('a', {'class': 'w-lightbox w-inline-block'}).get('href')
            cooking_item_image = requests.get(cooking_item_image_link).content
            with open(f'static/img/{cooking_item_name}.jpg', 'wb') as pic:
                pic.write(cooking_item_image)
            cooking_item_image_link = f'static/img/{cooking_item_name}.jpg'
            cooking_description = cooking_page.find('span', {'itemprop': 'description'}).text
            cooking_time = cooking_page.find('span', {'class': 'rcooktimetext'}).text
            cooking_ingredients = cooking_page.find_all('div', {'class': 'inglist'})
        except AttributeError:
            cooking_description = ''
            cooking_time = '0'

        for ingredients in cooking_ingredients:
            ingredients_values = ingredients.text.split(' — ')
            if len(ingredients_values) <= 1:
                ingredients_values.append('')
            cooking_ingredients_dict[ingredients_values[0]] = ingredients_values[1]

        preparation = cooking_page.find_all('div', {'itemprop': 'recipeInstructions'})

        count_offers = 1

        for preparation_element in preparation:
            try:
                offers = preparation_element.find_all('p')[-1].text
                if len(offers) > 1:
                    offers = preparation_element.find_all('p')[1].text

                cooking_step_by_step_dict[count_offers] = offers
                count_offers += 1
            except IndexError:
                count_except = 0
                if count_except == 0:
                    for except_offer in preparation_element:
                        cooking_step_by_step_dict[count_offers] = except_offer
                        count_except += 1
        cook_time = re.findall(r'\d+', cooking_time)

        dishes, created = Dishes.objects.get_or_create(
            title=cooking_item_name,
            image=cooking_item_image_link,
            description=cooking_description,
            cooking_time=int(cook_time[0]),
            link=cooking_link,
            dish_type=cooking_info['type'],
        )
        dishes.save()
        for ingredient, gram in cooking_ingredients_dict.items():
            print(ingredient)
            ing, cr = Ingredient.objects.get_or_create(
                title=ingredient,
                grammar=gram,
            )
            ing.save()
            dishes.ingredients.add(ing)
        for step, step_desc in cooking_step_by_step_dict.items():
            print(f'step: {step}, desc: {step_desc}')
            recipe, cr = Recipe.objects.get_or_create(
                step_position=step,
                step_text=str(step_desc)
            )
            recipe.save()
            dishes.recipes.add(recipe)
        if created == False:
            print('------->Created<-------')
        else:
            print('------->Saved<-------')

        print(num)
        num += 1

        cooking_ingredients_dict = dict()
        cooking_step_by_step_dict = dict()
        print('---------------------------------------------')
