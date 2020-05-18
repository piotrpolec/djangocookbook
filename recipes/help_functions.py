from .models import Recipe, Category, IngredientInstance, Ingredient, Step
from recipes import help_classes as hc
import folium


def add_to_database(name, difficulty, image, step_list, ing_list, cat_list, country, user):
    ingredients = []

    recipe = Recipe(name=name, difficulty=difficulty, image=image, country=country, made_by=user)
    recipe.save()
    for idx, step in enumerate(step_list):
        recipe.step_set.create(number=(idx+1), text=step)

    for ing in Ingredient.objects.all():
        ingredients.append(ing.return_name())
    for ing in ing_list:
        if ing[0] not in ingredients:
            ingredient = Ingredient(name=ing[0])
            ingredient.save()
        else:
            ingredient = Ingredient.objects.get(name=ing[0])
        ii = ingredient.ingredientinstance_set.create(how_much=ing[1], how_much_of_what=ing[2])
        ii.recipe.add(recipe)

    categories = []
    for cat in Category.objects.all():
        categories.append(cat.return_category())
    for cat in cat_list:
        if cat not in categories:
            category = Category(category=cat)
            category.save()
        else:
            category = Category.objects.get(category=cat)
        category.recipe.add(recipe)


def make_map(country_name):
    recipe_map = folium.Map()
    country_list = make_country_list()
    country = country_list.find_country_by_name(country_name)
    if country is not None and country.get_name() != "Inny":
        folium.Marker(location=[country.get_first_cord(), country.get_second_cord()]).add_to(recipe_map)
        return recipe_map._repr_html_()
    else:
        return None


list_of_countries = [
    hc.Country("Polska", (52.13, 21.00)),
    hc.Country("Austria", (42.30, 1.30)),
    hc.Country("Białoruś", (53.54, 27.33)),
    hc.Country("Bułgaria", (42.41, 23.19)),
    hc.Country("Czechy", (50.05, 15.25)),
    hc.Country("Dania", (55.40, 12.34)),
    hc.Country("Finlandia", (60.10, 24.56)),
    hc.Country("Francja", (48.52, 2.21)),
    hc.Country("Grecja", (38.00, 23.43)),
    hc.Country("Hiszpania", (40.23, -3.41)),
    hc.Country("Holandia", (52.22, 4.54)),
    hc.Country("Irlandia", (53.20, -6.15)),
    hc.Country("Niemcy", (52.31, 13.24)),
    hc.Country("Norwegia", (59.54, 10.44)),
    hc.Country("Protugalia", (38.42, -9.11)),
    hc.Country("Rosja", (55.45, 37.37)),
    hc.Country("Słowacja", (48.08, 17.06)),
    hc.Country("Szwajcaria", (59.20, 18.03)),
    hc.Country("Turcja", (39.56, 32.51)),
    hc.Country("Ukraina", (50.27, 30.30)),
    hc.Country("Węgry", (47.30, 19.03)),
    hc.Country("Wielka Brytania", (51.30, 0.07)),
    hc.Country("Włochy", (41.53, 12.29)),
    hc.Country("USA", (38.53, -75.2)),
    hc.Country("Inny", (0.0, 0.0))
]


def make_country_list():
    country_list = hc.CountryList()
    for country in list_of_countries:
        country_list.add_country(country)
    return country_list
