from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import FarmerSerializer
from .models import Farmer
from .filters import FarmerFilter
from local_directories.models import VillagesDirectory
from users.models import User
from utils.permissions import IsAdmin, IsSupervisor, IsSurveyor


class FarmerViewSet(viewsets.ModelViewSet):
    serializer_class = FarmerSerializer
    queryset = Farmer.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin|IsSupervisor|IsSurveyor]
    filterset_class = FarmerFilter
    search_fields = ['farmer_id', 'id_hash', 'name', 'phone_number']

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == 'list' and 'search' not in self.request.query_params:
            assigned_villages = None
            if self.request.user.user_type != User.UserType.ADMIN:
                assigned_blocks = [user_block.block for user_block in self.request.user.assigned_blocks.all()]
                assigned_villages = VillagesDirectory.objects.filter(block__in=assigned_blocks)

            if assigned_villages:
                queryset = queryset.filter(village__in=assigned_villages)

        return queryset

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user, last_edited_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(last_edited_by=self.request.user)
