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
from users.urls import router as users_router
from auth.urls import urlpatterns as auth_urlpatterns
from projects.urls import urlpatterns as projects_urlpatterns
from local_directories.urls import urlpatterns as local_directory_urlpatterns
from farmers.urls import router as farmers_router
from land_parcels.urls import router as land_parcels_router


urlpatterns = [
    path('', include(auth_urlpatterns)),
    path('', include(users_router.urls)),
    path('', include(local_directory_urlpatterns)),
    path('', include(farmers_router.urls)),
    path('', include(land_parcels_router.urls)),
    path('', include(projects_urlpatterns)),
]