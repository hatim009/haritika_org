from django_filters import rest_framework as filters
from django_filters.constants import EMPTY_VALUES

from users.models import UserProjectBlock
from projects.models import Project


class UserProjectFilter(filters.Filter):

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        
        filter_values = [int(filter_value.strip()) for filter_value in value.strip().split(',')]
        projects = Project.objects.filter(id__in=filter_values)

        user_ids = [user_project_block.user.id for user_project_block in UserProjectBlock.objects.filter(project__in=projects).distinct('user')]        
        
        return qs.filter(id__in=user_ids)