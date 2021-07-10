from rest_framework import serializers

from .models import Recipe, Tag, Ingredient


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        lookup_field = 'slug'


class IngridientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        lookup_field = 'title'
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        lookup_field = 'title'
        fields = '__all__'
