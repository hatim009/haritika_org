from django_filters import rest_framework as filters
from django_filters.constants import EMPTY_VALUES

from users.models import UserBlock
from local_directories.models import BlocksDirectory


class UserBlockFilter(filters.Filter):

    def __init__(self, name=None, *args, **kwargs):
        self.name = name
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        
        blocks = []
        filter_values = [int(filter_value.strip()) for filter_value in value.strip().split(',')]
        match self.name:
            case 'states':
                blocks = BlocksDirectory.objects.filter(district__state__in=filter_values)
            case 'districts':
                blocks = BlocksDirectory.objects.filter(district__in=filter_values)
            case 'blocks':
                blocks = BlocksDirectory.objects.filter(code__in=filter_values)
            case _:
                return qs

        user_ids = [user_block.user.id for user_block in UserBlock.objects.filter(block__in=blocks).distinct('user')]        
        
        return qs.filter(id__in=user_ids)