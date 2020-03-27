from django.db import models

# Create your models here.


class Recipe(models.Model):
    difficulty = models.IntegerField(default=1)
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=200) #link do obrazka

    def __str__(self):
        return self.name


class Category(models.Model):
    recipe = models.ManyToManyField(Recipe)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class IngredientInstance(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.DO_NOTHING)
    how_much = models.FloatField(default=0)
    how_much_of_what = models.CharField(max_length=10, default="")
    recipe = models.ManyToManyField(Recipe)

    def __str__(self):
        return self.ingredient.name + " " + str(self.how_much) + " " + self.how_much_of_what


class Steps(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.DO_NOTHING)
    number = models.IntegerField()
    text = models.CharField(max_length=200)

    def __str__(self):
        return str(self.number) + " " + self.text