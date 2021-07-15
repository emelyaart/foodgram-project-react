from rest_framework import filters as f
from django_filters.rest_framework import FilterSet, filters


class IngredientSearchFilter(f.SearchFilter):
    search_param = 'name'


class TagFilter(FilterSet):
    tags = filters.CharFilter(
        field_name='tags__slug',
        lookup_expr='iexact'
    )

    class Meta:
        fields = ['tags']
