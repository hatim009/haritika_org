import sys
import json

from django.core.management.base import BaseCommand, CommandError
from projects.models import Project
from projects.serializers import ProjectSerializer


class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            projects = Project.objects.all()
            project_serializer = ProjectSerializer(projects, many=True)
            print(json.dumps(project_serializer.data, indent=4))
                            
        except RuntimeError:
            raise CommandError('Error listing projects').with_traceback(sys.exception().__traceback__)