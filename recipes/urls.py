from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('<int:recipe_id>/', views.detail, name = 'detail'),
    path('categories', views.categories, name = "categories"),
    path('categories/<int:category_id>/', views.category, name = "category")

]