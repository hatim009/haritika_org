from django.db import transaction
from rest_framework import serializers
from .models import Farmer
from users.serializers import UserSerializer
from files_manager.serializers import FileSerializer
from local_directories.serializers import VillagesDirectorySerializer


from collections.abc import Mapping
from django.core.exceptions import ValidationError  as DjangoValidationError
from django.core.exceptions import ValidationError 
from rest_framework.settings import api_settings
from collections import OrderedDict
from rest_framework.fields import SkipField
from rest_framework.fields import get_error_detail, set_value


class FarmerSerializer(serializers.ModelSerializer):
    profile_photo = FileSerializer()
    id_front_image = FileSerializer()
    id_back_image = FileSerializer()
    village = VillagesDirectorySerializer()
    added_by = UserSerializer(read_only=True)
    last_edited_by = UserSerializer(read_only=True)

    class Meta:
        model = Farmer
        fields = '__all__'
        depth = 4
        read_only_fields = ['added_by', 'added_on', 'last_edited_by', 'last_edited_on']

    def create(self, validated_data):
        with transaction.atomic():
            validated_data['profile_photo'] = self.fields['profile_photo'].create(validated_data['profile_photo'])
            validated_data['id_front_image'] = self.fields['id_front_image'].create(validated_data['id_front_image'])
            validated_data['id_back_image'] = self.fields['id_back_image'].create(validated_data['id_back_image'])
            farmer = Farmer(**validated_data)
            farmer.save()
            return farmer
