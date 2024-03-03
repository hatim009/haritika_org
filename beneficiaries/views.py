from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from beneficiaries.serializers import BeneficiarySerializer
from beneficiaries.models import Beneficiary
from beneficiaries.filters import BeneficiaryFilter

from farmers.models import Farmer
from users.models import User
from local_directories.models import VillagesDirectory
from .permissions import IsAdmin, IsSupervisor, IsSurveyor


class BeneficiaryViewset(viewsets.ModelViewSet):
    serializer_class = BeneficiarySerializer
    queryset = Beneficiary.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin|IsSupervisor|IsSurveyor]
    filterset_class = BeneficiaryFilter
    search_fields = ['beneficiary_id', 'id_hash', 'name', 'phone_number', 'guardian__farmer_id', 'guardian__id_hash', 'guardian__name', 'guardian__phone_number']

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
        farmer = Farmer.objects.get(pk=self.request.data['guardian'])
        serializer.save(guardian=farmer, added_by=self.request.user, last_edited_by=self.request.user)

    def perform_update(self, serializer):
        farmer = Farmer.objects.get(pk=self.request.data['farmer_id'])
        serializer.save(guardian=farmer, last_edited_by=self.request.user)
