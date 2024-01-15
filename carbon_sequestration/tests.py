from django_filters import rest_framework as filters

from beneficiaries.models import Beneficiary
from filters import MultiValueFilter


class CarbonSequestrationFilter(filters.FilterSet):
    villages = MultiValueFilter(field_name='land_parcel', lookup_expr='village__in')
    blocks = MultiValueFilter(field_name='land_parcel', lookup_expr='village__block__in')
    districts = MultiValueFilter(field_name='land_parcel', lookup_expr='village__block__district__in')
    states = MultiValueFilter(field_name='land_parcel', lookup_expr='village__block__district__state__in')
    
    class Meta:
        model = Beneficiary
        fields = ['villages', 'blocks', 'districts', 'states']
