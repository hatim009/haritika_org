from django_filters import rest_framework as filters

from users.models import User
from .user_block_filter import UserBlockFilter
from .user_project_fiter import UserProjectFilter


class UserFilter(filters.FilterSet):
    user_type = filters.CharFilter()
    blocks = UserBlockFilter(name='blocks')
    districts = UserBlockFilter(name='districts')
    states = UserBlockFilter(name='states')
    projects = UserProjectFilter()
    
    class Meta:
        model = User
        fields = ['user_type', 'blocks', 'districts', 'states']
