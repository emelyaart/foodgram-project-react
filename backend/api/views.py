from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination

from .models import Tag
from .serializers import TagSerializer
from .permissions import IsStaffOrReadOnly


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    lookup_field = 'slug'
