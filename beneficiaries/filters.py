from django_filters import rest_framework as filters

from .models import Beneficiary
from utils.filters import MultiValueFilter


class BeneficiaryFilter(filters.FilterSet):
    villages = MultiValueFilter(field_name='village', lookup_expr='in')
    blocks = MultiValueFilter(field_name='village', lookup_expr='block__in')
    districts = MultiValueFilter(field_name='village', lookup_expr='block__district__in')
    states = MultiValueFilter(field_name='village', lookup_expr='block__district__state__in')
    
    class Meta:
        model = Beneficiary
        fields = ['villages', 'blocks', 'districts', 'states']
