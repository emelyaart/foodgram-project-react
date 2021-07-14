from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from users.models import CustomUser

from .models import Ingredient, IngredientAmount, Recipe, Tag


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientAmountSerializer(serializers.ModelSerializer):

    class Meta:
        model = IngredientAmount
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'image', 'text',
                  'ingredients', 'cooking_time')
        depth = 1

    def create(self, validated_data):
        image = validated_data.pop('image')
        recipe = Recipe.objects.create(image=image, **validated_data)
        data = self.context.get('request').data
        ingredients_data = data.get('ingredients')
        tags_data = data.get('tags')
        for tag_id in tags_data:
            tag_obj = Tag.objects.get(pk=tag_id)
            recipe.tags.add(tag_obj)
        for ingredient in ingredients_data:
            ingredient_amount_obj = IngredientAmount.objects.create(
                recipe=recipe,
                ingredients_id=ingredient.get('id'),
                amount=ingredient.get('amount')
            )
            ingredient_amount_obj.save()
        return recipe
