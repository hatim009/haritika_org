import json
from collections import OrderedDict

from django.core.exceptions import ValidationError
from rest_framework import serializers

from carbon_sequestration.models import CarbonSequestrationProgress, CarbonSequestrationModel



class CarbonSequestrationProgressListSerializer(serializers.ListSerializer):
    PROGRESS_FIELD_NAME = 'progress'

    def to_internal_value(self, data):
        if self.PROGRESS_FIELD_NAME not in data:
            raise ValidationError([{self.PROGRESS_FIELD_NAME: ['This field is required.']}])
        
        ret = super().to_internal_value(json.loads(data[self.PROGRESS_FIELD_NAME]))

        errors = OrderedDict()
        for progress in ret:
            carbon_sequestration_id_model = '-'.join([str(progress['carbon_sequestration'].id), progress['model'].name])

            if carbon_sequestration_id_model not in self.instance:
                errors[carbon_sequestration_id_model] = [
                    'Invalid model %s for carbon_sequestration id %s' % (progress['model'], progress['carbon_sequestration'])
                ]

        if errors:
            errors['active_models'] =  [progress.model.name for id, progress in self.instance.items()]
            raise ValidationError([errors])

        return ret

    def create(self, carbon_sequestration):
        models = CarbonSequestrationModel.objects.filter(is_active=True)
        progress = [CarbonSequestrationProgress(carbon_sequestration=carbon_sequestration, model=model) for model in models]

        return CarbonSequestrationProgress.objects.bulk_create(progress)
    
    def update(self, instance, validated_data):
        updated_instance = []
        for progress in validated_data:
            carbon_sequestration_id_model = '-'.join([str(progress['carbon_sequestration'].id), progress['model'].name])
            updated_instance.append(self.child.update(instance[carbon_sequestration_id_model], progress))

        return updated_instance


class CarbonSequestrationProgressSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarbonSequestrationProgress
        fields = '__all__'
        list_serializer_class = CarbonSequestrationProgressListSerializer
        # This is to override UniqueTogetherValidator coming from CarbonSequestrationProgress model.
        validators = []
