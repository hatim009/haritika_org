from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from carbon_sequestration.serializers import CarbonSequestrationSerializer, CarbonSequestrationProgressSerializer
from carbon_sequestration.models import CarbonSequestration
from carbon_sequestration.filters import CarbonSequestrationFilter
from .permissions import IsAdmin, IsSupervisor, IsSurveyor

class CarbonSequestrationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin|IsSupervisor|IsSurveyor]
    serializer_class = CarbonSequestrationSerializer
    queryset = CarbonSequestration.objects.all()
    filterset_class = CarbonSequestrationFilter
    search_fields = ['land_parcel__farmer', 'land_parcel__framer__phone_number', 'land_parcel__framer__id_hash', 'land_parcel__framer__name', 'land_parcel']

    @action(detail=True, methods=['put'], name='Update model progress')
    def progress(self, request, pk=None):
        carbon_sequestration = self.get_object()
        progress_id_instance_map = {'-'.join([str(progress.carbon_sequestration.id), progress.model.name]): progress for progress in carbon_sequestration.progress.all()}
        carbon_sequestration_progress_serializer = CarbonSequestrationProgressSerializer(instance=progress_id_instance_map, data=request.data, many=True, source='progress')
        if carbon_sequestration_progress_serializer.is_valid():
            carbon_sequestration_progress_serializer.save()
            return Response({'progress': carbon_sequestration_progress_serializer.data})
        else:
            return Response(carbon_sequestration_progress_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
