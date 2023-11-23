"""
URL configuration for projectngo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from rest_framework.authtoken import views
from users.urls import router as users_router
from local_directories.urls import urlpatterns as local_directory_urlpatterns
from farmers.urls import router as farmers_router


urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('', include(users_router.urls)),
    path('', include(local_directory_urlpatterns)),
    path('', include(farmers_router.urls)),
]