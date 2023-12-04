from django.urls import path
from .views import obtain_user_auth_token


urlpatterns = [
    path('api-token-auth/', obtain_user_auth_token),
]