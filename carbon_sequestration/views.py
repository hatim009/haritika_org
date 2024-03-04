from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from carbon_sequestration.serializers import CarbonSequestrationSerializer, CarbonSequestrationProgressSerializer
from carbon_sequestration.models import CarbonSequestration
from carbon_sequestration.filters import CarbonSequestrationFilter
from .permissions import IsAdmin, IsSupervisor, IsSurveyor
from users.models import User
from local_directories.models import VillagesDirectory


class CarbonSequestrationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin|IsSupervisor|IsSurveyor]
    serializer_class = CarbonSequestrationSerializer
    queryset = CarbonSequestration.objects.all()
    filterset_class = CarbonSequestrationFilter
    search_fields = ['land_parcel__farmer__farmer_id', 'land_parcel__farmer__phone_number', 'land_parcel__farmer__id_hash', 'land_parcel__farmer__name', 'land_parcel__id']

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == 'list' and 'search' not in self.request.query_params:
            assigned_villages = None
            if self.request.user.user_type != User.UserType.ADMIN:
                assigned_blocks = [user_block.block for user_block in self.request.user.assigned_blocks.all()]
                assigned_villages = VillagesDirectory.objects.filter(block__in=assigned_blocks)

            if assigned_villages:
                queryset = queryset.filter(land_parcel__village__in=assigned_villages)

        return queryset

    @action(detail=True, methods=['put'], name='Update model progress')
    def progress(self, request, pk=None):
        carbon_sequestration = self.get_object()
        progress_id_instance_map = {'-'.join([str(progress.carbon_sequestration.id), progress.model.name]): progress for progress in carbon_sequestration.progress.all() if progress.model.is_active}
        carbon_sequestration_progress_serializer = CarbonSequestrationProgressSerializer(instance=progress_id_instance_map, data=request.data, many=True, source='progress')
        if carbon_sequestration_progress_serializer.is_valid():
            carbon_sequestration_progress_serializer.save()
            return Response({'progress': carbon_sequestration_progress_serializer.data})
        else:
            return Response(carbon_sequestration_progress_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['put'], name='Conclude a Carbon Sequestration Project')
    def conclude(self, request, pk=None):
        carbon_sequestration = self.get_object()
        carbon_sequestration.is_active = False
        carbon_sequestration.save()

    @action(detail=True, methods=['put'], name='Restart a concluded Carbon Sequestration Project')
    def restart(self, request, pk=None):
        carbon_sequestration = self.get_object()
        carbon_sequestration.is_active = True
        carbon_sequestration.save()