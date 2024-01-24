from rest_framework import views
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Project
from .serializers import ProjectSerializer


class ProjectsView(views.APIView):

    def get(self, request):
        projects = Project.objects.all().order_by('id')
        project_serializer = ProjectSerializer(projects, many=True)
        return Response({'projects': project_serializer.data})



