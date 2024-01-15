from rest_framework import viewsets
from carbon_sequestration.serializers import CarbonSequestrationSerializer
from carbon_sequestration.models import CarbonSequestration
from carbon_sequestration.filters import CarbonSequestrationFilter


class CarbonSequestrationViewSet(viewsets.ModelViewSet):
    serializer_class = CarbonSequestrationSerializer
    queryset = CarbonSequestration.objects.all()
    filterset_class = CarbonSequestrationFilter
    search_fields = ['land_parcel__farmer', 'land_parcel__framer__phone_number', 'land_parcel__framer__id_hash', 'land_parcel__framer__name', 'land_parcel']
