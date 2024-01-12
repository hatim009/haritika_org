from django.db import transaction
from rest_framework import serializers
from .models import Farmer
from users.serializers import UserSerializer
from files_manager.serializers import FileSerializer
from local_directories.serializers import VillagesDirectorySerializer
from land_parcels.serializers import LandParcelSerializer


class FarmerSerializer(serializers.ModelSerializer):
    profile_photo = FileSerializer()
    id_front_image = FileSerializer()
    id_back_image = FileSerializer()
    village = VillagesDirectorySerializer(depth=4)
    added_by = UserSerializer(read_only=True)
    last_edited_by = UserSerializer(read_only=True)
    land_parcels = LandParcelSerializer(many=True, read_only=True, source='owned_land_parcels')

    class Meta:
        model = Farmer
        fields = '__all__'
        read_only_fields = ['added_by', 'added_on', 'last_edited_by', 'last_edited_on']

    def create(self, validated_data):
        with transaction.atomic():
            validated_data['profile_photo'] = self.fields['profile_photo'].create(validated_data['profile_photo'])
            validated_data['id_front_image'] = self.fields['id_front_image'].create(validated_data['id_front_image'])
            validated_data['id_back_image'] = self.fields['id_back_image'].create(validated_data['id_back_image'])
            
            farmer = Farmer(**validated_data)
            farmer.save()
            
            return farmer
    
    def update(self, instance, validated_data):
        with transaction.atomic():
            if validated_data.get('profile_photo'):
                self.fields['profile_photo'].update(instance.profile_photo, validated_data['profile_photo'])
            if validated_data.get('id_front_image'):
                self.fields['id_front_image'].update(instance.id_front_image, validated_data['id_front_image'])
            if validated_data.get('id_back_image'):
                self.fields['id_back_image'].update(instance.id_back_image, validated_data['id_back_image'])
            
            instance.name = validated_data.get('name', instance.name)
            instance.guardian_name = validated_data.get('guardian_name', instance.guardian_name)
            instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
            instance.phone_number = validated_data.get('phone_number', instance.phone_number)
            instance.category = validated_data.get('category', instance.category)
            instance.gender = validated_data.get('gender', instance.gender)
            instance.address = validated_data.get('address', instance.address)
            instance.village = validated_data.get('village', instance.village)
            instance.income_level = validated_data.get('income_level', instance.income_level)

            instance.save()
            
            return instance
