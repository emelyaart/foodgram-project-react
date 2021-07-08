from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination

from .models import Tag, Ingredient
from .serializers import TagSerializer, IngridientSerializer
from .permissions import IsStaffOrReadOnly


class BaseTagsAndIngridientViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


class TagsViewSet(BaseTagsAndIngridientViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug'


class IngridientsViewSet(BaseTagsAndIngridientViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngridientSerializer
