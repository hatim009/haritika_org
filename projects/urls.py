
from django.urls import path
from .views import *


urlpatterns = [
    path('projects/', ProjectsView.as_view()),
    path('projects/<int:project_id>/activate', ProjectsView.as_view())
]
