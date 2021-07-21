from django.db.models import Exists, OuterRef
from django.http import HttpResponse
from djoser.views import UserViewSet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import IngredientSearchFilter, TagFilter
from .mixins import BaseTagAndIngredientViewSet
from .models import (Cart, Favorite, Ingredient, IngredientAmount, Recipe,
                     Subscribe, Tag, User)
from .paginations import LimitPageNumberPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeMinifiedSerializer,
                          RecipeSerializer, SubscribeSerializer, TagSerializer)


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
    permission_classes = [IsAuthorOrReadOnly]

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

    @action(detail=True, permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        recipe = self.get_object()
        user = request.user

        return self.add_obj(Favorite, user, recipe)

    @favorite.mapping.delete
    def del_favorite(self, request, pk=None):
        user = request.user
        recipe = self.get_object()

        return self.delete_obj(Favorite, user, recipe)

    @action(detail=True, permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = self.get_object()

        return self.add_obj(Cart, user, recipe)

    @shopping_cart.mapping.delete
    def del_shopping_cart(self, request, pk=None):
        user = request.user
        recipe = self.get_object()

        return self.delete_obj(Cart, user, recipe)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        queryset = IngredientAmount.objects.filter(
            Exists(Recipe.objects.filter(
                Exists(Cart.objects.filter(
                    user=user)))))
        ingredients = {}
        for q in queryset:
            if q.ingredients.id not in ingredients:
                ingredients[q.ingredients.id] = {
                    'name': q.ingredients.name,
                    'amount': q.amount,
                    'measurement_unit': q.ingredients.measurement_unit
                }
            else:
                ingredients[q.ingredients.id]['amount'] += q.amount

        pdfmetrics.registerFont(TTFont('FiraSans', 'FiraSans.ttf', 'UTF-8'))
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_list.pdf"')
        page = canvas.Canvas(response)
        page.setFont('FiraSans', size=16)
        page.drawString(200, 800, 'Список ингредиентов')
        height = 750
        i = 1
        for item in ingredients.values():
            page.drawString(
                50,
                height,
                (f'{i}) { item["name"] } - {item["amount"]}, '
                 f'{item["measurement_unit"]}')
            )
            height -= 25
            i += 1
        page.showPage()
        page.save()
        return response

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

    @action(detail=True, permission_classes=[IsAuthenticated])
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

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = Subscribe.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
