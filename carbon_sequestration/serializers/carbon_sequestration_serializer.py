from collections import OrderedDict

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.db import transaction

from carbon_sequestration.models import CarbonSequestration
from land_parcels.serializers import LandParcelSerializer
from land_parcels.models import LandParcel
from files_manager.serializers import FileSerializer


class CarbonSequestrationSerializer(serializers.ModelSerializer):
    land_parcel = LandParcelSerializer(read_only=True)
    carbon_waiver_document = FileSerializer()
    agreement_document_type = FileSerializer()
    gram_panchayat_resolution = FileSerializer()

    class Meta:
        model = CarbonSequestration
        fields = '__all__'
        read_only_fields = ['total_pits_dug', 'total_pits_fertilized', 'total_pits_planted']

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)

        errors = OrderedDict()

        if not data.get('land_parcel'):
            errors['land_parcel'] = ['This field is required']
            raise ValidationError(errors)

        try:
            land_parcel = LandParcel.objects.get(pk=data['land_parcel'])
        except LandParcel.DoesNotExist:
            errors['land_parcel'] = ['LandParcel with id %s does not exists.' % (data['land_parcel'])]
            raise ValidationError(errors)
        else:
            ret['land_parcel'] = land_parcel

        return ret

    def create(self, validated_data):
        with transaction.atomic():
            validated_data['carbon_waiver_document'] = self.fields['carbon_waiver_document'].create(validated_data['carbon_waiver_document'])
            validated_data['agreement_document_type'] = self.fields['agreement_document_type'].create(validated_data['agreement_document_type'])
            validated_data['gram_panchayat_resolution'] = self.fields['gram_panchayat_resolution'].create(validated_data['gram_panchayat_resolution'])

            carbon_sequestration = CarbonSequestration(**validated_data)
            carbon_sequestration.save()

            return carbon_sequestration
        
    def update(self, carbon_sequestration, validated_data):
        with transaction.atomic():
            if validated_data.get('carbon_waiver_document'):
                self.fields['carbon_waiver_document'].update(carbon_sequestration.carbon_waiver_document, validated_data['carbon_waiver_document'])
            if validated_data.get('agreement_document_type'):
                self.fields['agreement_document_type'].update(carbon_sequestration.agreement_document_type, validated_data['agreement_document_type'])
            if validated_data.get('gram_panchayat_resolution'):
                self.fields['gram_panchayat_resolution'].update(carbon_sequestration.gram_panchayat_resolution, validated_data['gram_panchayat_resolution'])
            
            carbon_sequestration.total_pits_target = validated_data.get('total_pits_target', carbon_sequestration.total_pits_target)

            carbon_sequestration.save()
            
            return carbon_sequestration
