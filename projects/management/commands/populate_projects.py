import os
import csv
import sys

from django.core.management.base import BaseCommand, CommandError
from projects.models import Project

class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            projects_location = 'resources/projects/projects.csv'
            with open(projects_location, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    assert(len(row) == 1)

                    project, project_created = Project.objects.get_or_create(name=row['name'], is_active=False)
                    print('{0}: {1}\n'.format(project.name, project_created))
                            
        except RuntimeError:
            raise CommandError('Error populating projects').with_traceback(sys.exception().__traceback__)

        self.stdout.write(
            self.style.SUCCESS('Successfully populated projects!!!')
        )