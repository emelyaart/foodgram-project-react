from django.contrib import admin
from django.urls import path, include
from users.views import AuthToken

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/token/login/', AuthToken.as_view(), name='token')
]
