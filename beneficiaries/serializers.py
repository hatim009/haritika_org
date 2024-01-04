from django.db import transaction

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Beneficiary
from farmers.models import Farmer

from users.serializers import UserSerializer
from files_manager.serializers import FileSerializer


class BeneficiarySerializer(serializers.ModelSerializer):

    profile_photo = FileSerializer()
    id_front_image = FileSerializer()
    id_back_image = FileSerializer()
    added_by = UserSerializer(read_only=True)
    id_hash = serializers.CharField(min_length=128, max_length=128, validators=[UniqueValidator(queryset=Farmer.objects.all()), UniqueValidator(queryset=Beneficiary.objects.all())])

    class Meta:
        model = Beneficiary
        fields = '__all__'
        read_only_fields = ['added_by', 'added_on', 'last_edited_by', 'last_edited_on']
        parent_attribute = 'guardian'

    def create(self, validated_data):
        with transaction.atomic():
            validated_data['profile_photo'] = self.fields['profile_photo'].create(validated_data['profile_photo'])
            validated_data['id_front_image'] = self.fields['id_front_image'].create(validated_data['id_front_image'])
            validated_data['id_back_image'] = self.fields['id_back_image'].create(validated_data['id_back_image'])
            
            beneficiary = Beneficiary(**validated_data)
            beneficiary.save()
            
            return beneficiary
        
        
    def update(self, instance, validated_data):
        with transaction.atomic():
            if validated_data.get('profile_photo'):
                self.fields['profile_photo'].update(instance.profile_photo, validated_data['profile_photo'])
            if validated_data.get('id_front_image'):
                self.fields['id_front_image'].update(instance.id_front_image, validated_data['id_front_image'])
            if validated_data.get('id_back_image'):
                self.fields['id_back_image'].update(instance.id_back_image, validated_data['id_back_image'])
            
            instance.name = validated_data.get('name', instance.name)
            instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
            instance.phone_number = validated_data.get('phone_number', instance.phone_number)
            instance.gender = validated_data.get('gender', instance.gender)
            instance.address = validated_data.get('address', instance.address)
            instance.village = validated_data.get('village', instance.village)

            instance.save()
            
            return instance