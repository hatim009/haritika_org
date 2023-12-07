from rest_framework import viewsets
from django.db import transaction

from auth.permissions import IsAdmin
from .models import LandParcel
from .serializers import LandParcelSerializer
from farmers.models import Farmer


class LandParcelViewSet(viewsets.ModelViewSet):
    permssion_classes = [IsAdmin]
    serializer_class = LandParcelSerializer
    queryset = LandParcel.objects.all()

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