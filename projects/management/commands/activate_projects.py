import os
import csv
import sys

from django.core.management.base import BaseCommand, CommandError
from projects.models import Project
from django.db import transaction

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--projects', type=str, required=True)

    def handle(self, *args, **options):
        try:
            project_ids = [int(project_id.strip()) for project_id in options['projects'].strip().split(',')]
            projects = Project.objects.filter(id__in=project_ids)

            valid_projects = [project.id for project in projects]
            invalid_projects = [project_id for project_id in project_ids if project_id not in valid_projects]

            with transaction.atomic():
                for project in projects:
                    project.is_active = True
                    project.save()

            if invalid_projects:
                raise CommandError('Invalid project ids: %s' % invalid_projects)
                            
        except RuntimeError:
            raise CommandError('Error activating projects').with_traceback(sys.exception().__traceback__)

        self.stdout.write(
            self.style.SUCCESS('Successfully activated following projects:\n%s' % project_ids)
        )