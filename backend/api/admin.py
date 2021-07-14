from django.contrib import admin

from .models import Ingredient, Recipe, Tag


class IngredientAmountInline(admin.TabularInline):
    model = Ingredient.recipes.through


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'author']
    inlines = [IngredientAmountInline]
