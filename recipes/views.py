from django.shortcuts import get_object_or_404,render,redirect
from django.template import loader
from django.http import HttpResponse
from .models import Recipe, Category
from django.http import Http404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


def home(request):
    return render(request, 'Registration/home.html')


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
        'step' : recipe.step_set.all().order_by('number'),
        'categories' : recipe.category_set.all(),
        'range_for_stars': range(recipe.difficulty),
        'range_for_rest_stars': range(recipe.difficulty+1, 6),
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


def signup(request):
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
    return render(request, 'Registration/signup.html', {'form': form})