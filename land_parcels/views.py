from django.db import transaction
from django.db.models import Q

from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from utils.permissions import IsAdmin, IsSupervisor, IsSurveyor
from .models import LandParcel
from .serializers import LandParcelSerializer
from .filters import LandParcelFilter
from farmers.models import Farmer
from users.models import User
from local_directories.models import VillagesDirectory


class LandParcelViewSet(viewsets.ModelViewSet):
    permssion_classes = [IsAuthenticated, IsAdmin|IsSupervisor|IsSurveyor]
    serializer_class = LandParcelSerializer
    queryset = LandParcel.objects.all()
    filterset_class = LandParcelFilter
    search_fields = ['id', 'farmer__farmer_id', 'farmer__id_hash', 'farmer__name', 'farmer__phone_number']

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
        farmer = Farmer.objects.get(pk=self.request.data['farmer_id'])
        serializer.save(farmer=farmer, added_by=self.request.user, last_edited_by=self.request.user)

    def perform_update(self, serializer):
        farmer = Farmer.objects.get(pk=self.request.data['farmer_id'])
        serializer.save(farmer=farmer, last_edited_by=self.request.user)
    
    def perform_destroy(self, instance):
        with transaction.atomic():
            for land_parcel_picture in instance.land_parcel_pictures.all():
                land_parcel_picture.picture.delete()
            instance.delete()   