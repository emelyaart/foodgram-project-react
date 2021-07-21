from rest_framework import viewsets, mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from djoser.views import UserViewSet
from django.db.models import OuterRef, Exists

from .models import Cart, Favorite, Recipe, Subscribe, Tag, Ingredient, User
from .serializers import (SubscribeSerializer, TagSerializer,
                          IngredientSerializer, RecipeSerializer,
                          RecipeMinifiedSerializer)
from .permissions import IsAuthorOrReadOnly, IsStaffOrReadOnly
from .filters import IngredientSearchFilter, TagFilter
from .paginations import LimitPageNumberPagination


class BaseTagAndIngredientViewSet(mixins.ListModelMixin,
                                  mixins.RetrieveModelMixin,
                                  viewsets.GenericViewSet):
    permission_classes = [IsStaffOrReadOnly]


class TagsViewSet(BaseTagAndIngredientViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(BaseTagAndIngredientViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [IngredientSearchFilter]
    search_fields = ['^name']


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LimitPageNumberPagination
    filter_class = TagFilter
    permission_classes = [IsAuthorOrReadOnly, IsStaffOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user
        )
        return serializer

    def get_queryset(self):
        user = self.request.user

        if self.request.GET.get('is_favorited'):
            return self.filter_obj(Favorite, user)
        elif self.request.GET.get('is_in_shopping_cart'):
            return self.filter_obj(Cart, user)

        return Recipe.objects.all()

    @action(methods=['get'], detail=True)
    def favorite(self, request, pk=None):
        recipe = Recipe.objects.get(pk=pk)
        user = request.user

        return self.add_obj(Favorite, user, recipe)

    @favorite.mapping.delete
    def del_favorite(self, request, pk=None):
        user = request.user
        recipe = self.get_object()

        return self.delete_obj(Favorite, user, recipe)

    @action(methods=['get'], detail=True)
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = self.get_object()

        return self.add_obj(Cart, user, recipe)

    @shopping_cart.mapping.delete
    def del_shopping_cart(self, request, pk=None):
        user = request.user
        recipe = self.get_object()

        return self.delete_obj(Cart, user, recipe)

    def add_obj(self, model, user, recipe):
        if model.objects.filter(user=user, recipe=recipe).exists():
            return Response({
                'errors': 'Рецепт уже добавлен в список'
            }, status=status.HTTP_400_BAD_REQUEST)

        obj = model.objects.create(
            user=user, recipe=recipe
        )
        obj.save()
        serializer = RecipeMinifiedSerializer(recipe)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_obj(self, model, user, recipe):
        obj = model.objects.filter(user=user, recipe=recipe)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({
            'errors': 'Рецепт уже удален'
        }, status=status.HTTP_400_BAD_REQUEST)

    def filter_obj(self, model, user):
        return Recipe.objects.annotate(
            is_filtered=Exists(
                model.objects.filter(
                    user=user, recipe_id=OuterRef('pk')
                )
            )
        ).filter(is_filtered=True)


class CustomUserViewSet(UserViewSet):
    pagination_class = LimitPageNumberPagination

    @action(methods=['get'], detail=True)
    def subscribe(self, request, id=None):
        user = request.user
        subscriber = get_object_or_404(User, id=id)

        if (Subscribe.objects.filter(user=user, subscriber=subscriber)
                .exists() or user == subscriber):
            return Response({
                'errors': ('Вы уже подписаны на этого пользователя '
                           'или подписываетесь на самого себя')
            }, status=status.HTTP_400_BAD_REQUEST)

        subscribe = Subscribe.objects.create(user=user, subscriber=subscriber)
        subscribe.save()
        serializer = SubscribeSerializer(
            subscribe, context={'request': request}
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def del_subscribe(self, request, id=None):
        user = request.user
        subscriber = get_object_or_404(User, id=id)
        subscribe = Subscribe.objects.filter(
            user=user, subscriber=subscriber
        )
        if subscribe.exists():
            subscribe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({
            'errors': 'Вы уже отписались'
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['get'],
        detail=False,
        pagination_class=LimitPageNumberPagination
    )
    def subscriptions(self, request):
        user = request.user
        subscribing = Subscribe.objects.filter(user=user)
        serializer = SubscribeSerializer(
            subscribing,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
