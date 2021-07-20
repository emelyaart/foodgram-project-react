from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .models import (Ingredient, IngredientAmount, Recipe, Subscribe, Tag,
                     Favorite, Cart, User)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
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
    id = serializers.ReadOnlyField(source='ingredients.id')
    name = serializers.ReadOnlyField(source='ingredients.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredients.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(
        source='ingredientamount_set',
        many=True,
        read_only=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')
        depth = 1

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        return Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        return Cart.objects.filter(user=user, recipe=obj).exists()

    def create(self, validated_data):
        image = validated_data.pop('image')
        recipe = Recipe.objects.create(image=image, **validated_data)
        data = self.context.get('request').data
        ingredients_data = data.get('ingredients')
        tags_data = data.get('tags')

        for tag_id in tags_data:
            recipe.tags.add(Tag.objects.get(pk=tag_id))

        for ingredient in ingredients_data:
            ingredient_amount_obj = IngredientAmount.objects.create(
                recipe=recipe,
                ingredients_id=ingredient.get('id'),
                amount=ingredient.get('amount')
            )
            ingredient_amount_obj.save()

        return recipe

    def update(self, instance, validated_data):
        data = self.context.get('request').data
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.tags.clear()
        IngredientAmount.objects.filter(recipe=instance).all().delete()
        tags_data = data.get('tags')

        for tag_id in tags_data:
            instance.tags.add(Tag.objects.get(pk=tag_id))

        for ingredient in data.get('ingredients'):
            ingredient_amount_obj = IngredientAmount.objects.create(
                recipe=instance,
                ingredients_id=ingredient.get('id'),
                amount=ingredient.get('amount')
            )
            ingredient_amount_obj.save()

        return instance


class RecipeMinifiedSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='subscriber.email')
    username = serializers.ReadOnlyField(source='subscriber.username')
    first_name = serializers.ReadOnlyField(source='subscriber.first_name')
    last_name = serializers.ReadOnlyField(source='subscriber.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscribe
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        return Subscribe.objects.filter(
            user=obj.get('user'), subscriber=obj.get('subscriber')
        ).exists()

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author=obj.get('subscriber'))
        return RecipeMinifiedSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.get('subscriber')).count()
