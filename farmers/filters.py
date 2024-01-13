from django_filters import rest_framework as filters

from farmers.models import Farmer
from filters import MultiValueFilter


class FarmerFilter(filters.FilterSet):
    villages = MultiValueFilter(field_name='village', lookup_expr='in')
    blocks = MultiValueFilter(field_name='village', lookup_expr='block__in')
    districts = MultiValueFilter(field_name='village', lookup_expr='block__district__in')
    states = MultiValueFilter(field_name='village', lookup_expr='block__district__state__in')
    
    class Meta:
        model = Farmer
        fields = ['villages', 'blocks', 'districts', 'states']
