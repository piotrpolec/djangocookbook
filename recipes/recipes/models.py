from django.db import models
from django.utils.translation import gettext_lazy as _


class Recipe(models.Model):
    class Difficulty(models.IntegerChoices):
        VERY_EASY = 1
        EASY = 2
        MEDIUM = 3
        HARD = 4
        VERY_HARD = 5
    difficulty = models.IntegerField(choices = Difficulty.choices, default = Difficulty.MEDIUM)
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=200) #link do obrazka

    def __str__(self):
        return self.name


class Category(models.Model):
    recipe = models.ManyToManyField(Recipe)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category

    def return_category(self):
        return str(self.category)


class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def return_name(self):
        return str(self.name)


class IngredientInstance(models.Model):
    class Measurement(models.TextChoices):
        PIECE = 'PSC'
        CUP = 'C'
        ML = 'ML'
        L = 'L'
        G = 'G'
        KG = 'KG'
        SPOON = 'SP'
        TEASPOON = 'TSP'
        PINCH = 'P'
        CLOVE = 'CLV'
    ingredient = models.ForeignKey(Ingredient, on_delete=models.DO_NOTHING)
    how_much = models.FloatField(default=0)
    how_much_of_what = models.CharField(choices = Measurement.choices, max_length = 5)
    recipe = models.ManyToManyField(Recipe)

    def __str__(self):
        return self.ingredient.name + " " + str(self.how_much) + " " + self.how_much_of_what

    def return_measurement(self):
        return self.Measurement.choices


class Step(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.DO_NOTHING)
    number = models.IntegerField()
    text = models.CharField(max_length=200)

    def __str__(self):
        return str(self.number) + " " + self.text