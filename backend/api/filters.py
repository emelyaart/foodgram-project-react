from django_filters.rest_framework import FilterSet, filters
from rest_framework import filters as f

from .models import Recipe


class IngredientSearchFilter(f.SearchFilter):
    search_param = 'name'


class TagFilter(FilterSet):
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug'
    )

    class Meta:
        model = Recipe
        fields = ['tags']
