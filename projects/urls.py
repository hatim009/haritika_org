
from django.urls import path
from .views import *


urlpatterns = [
    path('projects/', list_projects),
    path('projects/<int:project_id>/activate/', activate_project)
]
