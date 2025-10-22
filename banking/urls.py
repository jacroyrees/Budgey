from django.urls import path

from banking.views import PublicTokenCreate, AccessTokenCreate

urlpatterns = [
path('get_public_token/', PublicTokenCreate.as_view()),
path('get_access_token/', AccessTokenCreate.as_view()),
]