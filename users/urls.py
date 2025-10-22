from django.urls import path, include, re_path

from .views import (CustomTokenVerifyView, CustomTokenRefreshView, CustomTokenObtainPairView, LogoutView, CustomProviderAuthView)

urlpatterns = [
    re_path(r'^o/(?P<provider>\S+)/$', CustomProviderAuthView.as_view(), name='provider-auth'),
    path('jwt/create/', CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', CustomTokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', CustomTokenVerifyView.as_view(), name='jwt-verify'),
path('logout/', LogoutView.as_view(), name='logout'),

]