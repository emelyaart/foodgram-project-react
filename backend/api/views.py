from rest_framework import viewsets, mixins
from djoser.views import UserViewSet

from .models import Recipe, Tag, Ingredient
from .serializers import TagSerializer, IngredientSerializer, RecipeSerializer
from .permissions import IsAuthorOrReadOnly, IsStaffOrReadOnly
from .filters import IngredientSearchFilter, TagFilter
from .paginations import LimitPageNumberPagination


class TagsViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsStaffOrReadOnly]


class IngredientsViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsStaffOrReadOnly]
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


class CustomUserViewSet(UserViewSet):
    pagination_class = LimitPageNumberPagination
