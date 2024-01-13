from django_filters import rest_framework as filters
from django_filters.constants import EMPTY_VALUES


class MultiValueFilter(filters.Filter):

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        
        filter_values = [int(filter_value.strip()) for filter_value in value.strip().split(',')]

        return super().filter(qs, filter_values)