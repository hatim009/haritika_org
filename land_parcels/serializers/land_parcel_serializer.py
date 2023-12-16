from django.db import transaction
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.fields import empty
from land_parcels.models import LandParcel
from .land_parcel_picture_serializer import LandParcelPictureSerializer
from local_directories.serializers import VillagesDirectorySerializer
from users.serializers import UserSerializer


class LandParcelSerializer(serializers.ModelSerializer):

    pictures = LandParcelPictureSerializer(many=True, source='land_parcel_pictures')
    village = VillagesDirectorySerializer()
    added_by = UserSerializer(read_only=True)
    last_edited_by = UserSerializer(read_only=True)

    class Meta:
        model = LandParcel
        fields = '__all__'
        read_only_fields = ['farmer']

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(instance=instance, *args, **kwargs)
        if self.context.get('request') and self.context['request'].method in ['PUT', 'PATCH']:
            self.fields['pictures'].set_instance(instance, instance.land_parcel_pictures.all())

    def create(self, validated_data):
        with transaction.atomic():
            pictures = validated_data.pop('land_parcel_pictures')
            
            land_parcel = LandParcel(**validated_data)
            land_parcel.save()
            
            self.fields['pictures'].create(land_parcel, pictures)
            
            return land_parcel
    
    def update(self, land_parcel, validated_data):
        with transaction.atomic():
            if validated_data.get('land_parcel_pictures'):
                self.fields['pictures'].update(land_parcel.land_parcel_pictures.all(), validated_data['land_parcel_pictures'])
            
            land_parcel.ownership_type = validated_data.get('ownership_type', land_parcel.ownership_type)
            land_parcel.geo_trace = validated_data.get('geo_trace', land_parcel.geo_trace)
            land_parcel.area = validated_data.get('area', land_parcel.area)
            land_parcel.khasra_number = validated_data.get('khasra_number', land_parcel.khasra_number)
            land_parcel.farm_workers = validated_data.get('farm_workers', land_parcel.farm_workers)
            land_parcel.village = validated_data.get('village', land_parcel.village)

            land_parcel.save()
            
            return land_parcel
