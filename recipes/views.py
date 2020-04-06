from django.shortcuts import get_object_or_404,render
from django.template import loader
from django.http import HttpResponse
from .models import Recipe, Category
from django.http import Http404


def index(request):
    recipes = Recipe.objects.all()
    context = {
        'recipes': recipes,
    }
    return render(request, 'recipes/index.html', context)


def detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    context = {
        'name' : recipe.name,
        'difficulty' : recipe.difficulty,
        'image' : recipe.image,
        'steps' : recipe.steps_set.all().order_by('number'),
        'categories' : recipe.category_set.all(),
    }
    return render(request, 'recipes/detail.html', context)
    
def categories(request):
    categories = Category.objects.all()
    context = {
        'categories' : categories,
    }
    return render(request, 'categories/index.html', context)

def category(request, category_id):
    category = get_object_or_404(Category, pk = category_id)
    context = {
        'category' : category,
        'recipes' : category.recipe.all()
    }
    return render(request, 'categories/detail.html', context)