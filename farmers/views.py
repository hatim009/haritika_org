from django.db.models import Q

from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from .serializers import FarmerSerializer
from .models import Farmer
from local_directories.models import VillagesDirectory
from users.models import User
from .permissions import hasBlockPermission
from rest_framework.permissions import IsAuthenticated


class FarmerViewSet(viewsets.ModelViewSet):
    serializer_class = FarmerSerializer
    queryset = Farmer.objects.all()
    filter_backends = [SearchFilter]
    permission_classes = [IsAuthenticated, hasBlockPermission]
    search_fields = ['farmer_id', 'id_hash', 'name', 'phone_number']

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == 'list':
            villages = None
            if 'states' in self.request.GET:
                states = [int(state.strip()) for state in self.request.GET['states'].strip().split(',')]
                villages = VillagesDirectory.objects.filter(block__district__state__in=states)
            elif 'districts' in self.request.GET:
                districts = [int(district.strip()) for district in self.request.GET['districts'].strip().split(',')]
                villages = VillagesDirectory.objects.filter(block__district__in=districts)
            elif 'blocks' in self.request.GET:
                blocks = [int(block.strip()) for block in self.request.GET['blocks'].strip().split(',')]
                villages = VillagesDirectory.objects.filter(block__in=blocks)
            elif 'villages' in self.request.GET:
                villages = [int(village.strip()) for village in self.request.GET['villages'].strip().split(',')]

            assigned_villages = None
            if self.request.user.user_type != User.UserType.ADMIN:
                assigned_blocks = [user_block.block for user_block in self.request.user.assigned_blocks.all()]
                assigned_villages = VillagesDirectory.objects.filter(block__in=assigned_blocks)

            if villages and assigned_villages:
                queryset = queryset.filter(Q(village__in=villages) & Q(village__in=assigned_villages))
            elif villages:
                queryset = queryset.filter(village__in=villages)
            elif assigned_villages:
                queryset = queryset.filter(village__in=assigned_villages)

        return queryset

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user, last_edited_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(last_edited_by=self.request.user)
