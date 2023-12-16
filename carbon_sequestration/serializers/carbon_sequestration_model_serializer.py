from rest_framework import serializers
from carbon_sequestration.models import CarbonSequestrationModel


class CarbonSequestrationModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarbonSequestrationModel
        fields = '__all__'