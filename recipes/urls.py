from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('search', views.search, name = 'search'),
    path('add_recipe', views.add_recipe, name = 'add_recipe'),
    path('add_recipe_form', views.add_recipe_form_sub, name = 'add_recipe_form'),
    path('random', views.random_recipe, name='random'),
    path('<int:recipe_id>/', views.detail, name = 'detail'),
    path('categories', views.categories, name = "categories"),
    path('category/<int:category_id>/', views.category, name = "category"),
]