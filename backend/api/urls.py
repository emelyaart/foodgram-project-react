from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TagsViewSet

app_name = 'api'

router = DefaultRouter()
router.register('tags', TagsViewSet)

urlpatterns = [
    path('', include(router.urls))
]
