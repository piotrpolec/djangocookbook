from .models import Recipe, Category, IngredientInstance, Ingredient, Step


def add_to_database(name, difficulty, image, step_list, ing_list, cat_list):
    ingredients = []
    ingredient = None

    recipe = Recipe(name=name, difficulty=difficulty, image=image)
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
    category = None
    for cat in Category.objects.all():
        categories.append(cat.return_category())
    for cat in cat_list:
        if cat not in categories:
            category = Category(category=cat)
            category.save()
        else:
            category = Category.objects.get(category=cat)
        category.recipe.add(recipe)


