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
from projects.urls import urlpatterns as projects_urlpatterns
from local_directories.urls import urlpatterns as local_directory_urlpatterns
from farmers.urls import router as farmers_router
from land_parcels.urls import router as land_parcels_router
from beneficiaries.urls import router as beneficiaries_router
from carbon_sequestration.urls import router as carbon_sequestration_router
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', include(users_router.urls)),
    path('', include(local_directory_urlpatterns)),
    path('', include(farmers_router.urls)),
    path('', include(land_parcels_router.urls)),
    path('', include(beneficiaries_router.urls)),
    path('', include(projects_urlpatterns)),
    path('', include(carbon_sequestration_router.urls)),
]