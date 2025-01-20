from django.urls import path, include
from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),  # This line should remain for browsable API
    path('shop/', include('shop.urls')),  # Your shop-related views
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
