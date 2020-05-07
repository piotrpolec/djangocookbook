from django.contrib import admin

# Register your models here.

from .models import Recipe
from .models import Ingredient
from .models import Category
from .models import IngredientInstance
from .models import Step

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Category)
admin.site.register(IngredientInstance)
admin.site.register(Step)
