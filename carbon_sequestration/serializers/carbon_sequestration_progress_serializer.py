import json
from collections import OrderedDict

from django.db import transaction
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
        with transaction.atomic():
            models = CarbonSequestrationModel.objects.filter(is_active=True)
            progress_serializers = [CarbonSequestrationProgress(carbon_sequestration=carbon_sequestration, model=model) for model in models]
            progress = CarbonSequestrationProgress.objects.bulk_create(progress_serializers)

            carbon_sequestration.total_pits_target = 0
            carbon_sequestration.total_pits_dug = 0
            carbon_sequestration.total_pits_fertilized = 0
            carbon_sequestration.total_pits_planted = 0

            for model_progress in progress:
                carbon_sequestration.total_pits_target += model_progress.total_pits_target
                carbon_sequestration.total_pits_dug += model_progress.total_pits_dug
                carbon_sequestration.total_pits_fertilized += model_progress.total_pits_fertilized
                carbon_sequestration.total_pits_planted += model_progress.total_pits_planted

            carbon_sequestration.save()

            return progress
    
    def update(self, instance, validated_data):
        with transaction.atomic():
            updated_instance = []

            carbon_sequestration = None
            for progress in validated_data:
                carbon_sequestration_id_model = '-'.join([str(progress['carbon_sequestration'].id), progress['model'].name])
                carbon_sequestration = instance[carbon_sequestration_id_model].carbon_sequestration
                updated_instance.append(self.child.update(instance[carbon_sequestration_id_model], progress))

            if carbon_sequestration is None:
                return updated_instance

            progress = [model_progress for model_progress in carbon_sequestration.progress.all() if model_progress.model.is_active]

            carbon_sequestration.total_pits_target = 0
            carbon_sequestration.total_pits_dug = 0
            carbon_sequestration.total_pits_fertilized = 0
            carbon_sequestration.total_pits_planted = 0

            for model_progress in progress:
                carbon_sequestration.total_pits_target += model_progress.total_pits_target
                carbon_sequestration.total_pits_dug += model_progress.total_pits_dug
                carbon_sequestration.total_pits_fertilized += model_progress.total_pits_fertilized
                carbon_sequestration.total_pits_planted += model_progress.total_pits_planted

            carbon_sequestration.save()

            return updated_instance
        


class CarbonSequestrationProgressSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarbonSequestrationProgress
        fields = '__all__'
        list_serializer_class = CarbonSequestrationProgressListSerializer
        # This is to override UniqueTogetherValidator coming from CarbonSequestrationProgress model.
        validators = []
