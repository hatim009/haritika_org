from django_filters import rest_framework as filters

from .models import CarbonSequestration
from filters import MultiValueFilter


class CarbonSequestrationFilter(filters.FilterSet):
    villages = MultiValueFilter(field_name='village', lookup_expr='in')
    blocks = MultiValueFilter(field_name='village', lookup_expr='block__in')
    districts = MultiValueFilter(field_name='village', lookup_expr='block__district__in')
    states = MultiValueFilter(field_name='village', lookup_expr='block__district__state__in')
    
    class Meta:
        model = CarbonSequestration
        fields = ['villages', 'blocks', 'districts', 'states']