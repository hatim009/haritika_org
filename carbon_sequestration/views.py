from rest_framework import viewsets
from carbon_sequestration.serializers import CarbonSequestrationSerializer
from carbon_sequestration.models import CarbonSequestration


class CarbonSequestrationViewSet(viewsets.ModelViewSet):
    serializer_class = CarbonSequestrationSerializer
    queryset = CarbonSequestration.objects.all()
