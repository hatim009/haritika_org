from rest_framework import views, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .models import Project
from .serializers import ProjectSerializer
from .permissions import IsAdmin, IsSupervisor, IsSurveyor
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin|IsSupervisor|IsSurveyor])
def list_projects(request):
    projects = Project.objects.all().order_by('id')
    project_serializer = ProjectSerializer(projects, many=True)
    return Response({'projects': project_serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdmin])
def activate_project(request, project_id):
    try :
        project = Project.objects.get(id=project_id)
        project.is_active = True
        project.save()

        return Response({'detail': 'Project %s activated successfully' % (project_id)})
    except Project.DoesNotExist as e:
        return Response({'detail': 'Invalid project id [%s]'% (project_id)}, status=status.HTTP_400_BAD_REQUEST)
