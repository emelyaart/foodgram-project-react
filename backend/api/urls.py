from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TagsViewSet, IngridientsViewSet

app_name = 'api'

router = DefaultRouter()
router.register('tags', TagsViewSet)
router.register('ingridients', IngridientsViewSet)

urlpatterns = [
    path('', include(router.urls))
]
