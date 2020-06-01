from django.shortcuts import get_object_or_404,render,redirect
from django.template import loader
from django.http import HttpResponse
from .models import Recipe, Category
from django.http import Http404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from recipes.models import IngredientInstance
from recipes import help_functions as hp
import random
import folium


def home(request):
    return render(request, 'registration/home.html')


def index(request):
    recipes = Recipe.objects.all()
    context = {
        'recipes': recipes,
    }
    return render(request, 'recipes/index.html', context)


def detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    context = {
        'name': recipe.name,
        'difficulty': recipe.difficulty,
        'image': recipe.image,
        'step': recipe.step_set.all().order_by('number'),
        'ingredients': recipe.ingredientinstance_set.all(),
        'categories': recipe.category_set.all(),
        'range_for_stars': range(recipe.difficulty),
        'range_for_rest_stars': range(recipe.difficulty+1, 6),
        "map": hp.make_map(recipe.country)
    }
    return render(request, 'recipes/detail.html', context)


def categories(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'categories/index.html', context)


def category(request, category_id):
    category = get_object_or_404(Category, pk = category_id)
    context = {
        'category': category,
        'recipes': category.recipe.all()
    }
    return render(request, 'categories/detail.html', context)


def signup(request):  #przesada przerzucać do nowej aplikacji
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def search(request):
    query = request.GET.get('q')
    query = query.split()
    final_query = '%('
    for word in query:
      final_query += word + '|' 
    final_query = final_query[0:-1]
    final_query += ')%'
    recipes = Recipe.objects.raw(
        """SELECT DISTINCT recipes_recipe.id, recipes_recipe.difficulty, recipes_recipe.name, recipes_recipe.image 
        FROM recipes_recipe 
        LEFT OUTER JOIN recipes_ingredientinstance_recipe ON (recipes_recipe.id = recipes_ingredientinstance_recipe.recipe_id) 
        INNER JOIN recipes_ingredientinstance ON recipes_ingredientinstance_recipe.ingredientinstance_id =  recipes_ingredientinstance.id
        INNER JOIN recipes_ingredient ON recipes_ingredientinstance.ingredient_id = recipes_ingredient.id
        WHERE (LOWER(recipes_recipe.name) SIMILAR TO (%s) 
        OR LOWER(recipes_ingredient.name) SIMILAR TO (%s))""", [final_query, final_query])
    context = {
        'recipes': recipes
    }
    return render(request, 'recipes/index.html', context)


def random_recipe(request):
    numbers = Recipe.objects.values_list('id', flat=True)
    return redirect('detail', recipe_id=random.choice(numbers))


def add_recipe(request):
    if request.user.is_authenticated:
        ii = IngredientInstance()
        country_list = hp.make_country_list()
        for country in country_list.get_country_list():
            print(country.get_name())
        context = {
            "measurement": ii.return_measurement(),
            "country_list": country_list.get_country_list()
        }
        return render(request, 'recipes/add_recipe.html', context)
    else:
        return render(request, 'badway/not_logged.html')


def add_recipe_form_sub(request):
    name = request.POST["name"]
    difficulty = request.POST["difficulty"]
    image = request.POST["image"]
    country = request.POST["Kraj"]
    steps_count = request.POST.get("i", False)
    step_list = []
    for idx in range(int(steps_count)):
        step_list.append(request.POST["step" + str(idx)])
    ingredient_count = request.POST.get("j", False)
    ingredients_list = []
    for idx in range(int(ingredient_count)):
        one_ingredient = (request.POST["ing" + str(idx)], request.POST["how_much" + str(idx)],
                          request.POST["select" + str(idx)])
        ingredients_list.append(one_ingredient)
    category_count = request.POST.get("cat", False)
    categories_list = []
    for idx in range(int(category_count)):
        categories_list.append(request.POST["cat" + str(idx)])
    hp.add_to_database(name, difficulty, image, step_list, ingredients_list, categories_list, country, request.user)
    return render(request, 'recipes/recipe_added.html')
