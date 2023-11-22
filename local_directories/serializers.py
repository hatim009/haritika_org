from rest_framework import serializers
from .models import StatesDirectory, DistrictsDirectory, BlocksDirectory, VillagesDirectory


class StatesDirectorySerializer(serializers.ModelSerializer):

    class Meta:
        model = StatesDirectory
        fields = '__all__'


class DistrictsDirectorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DistrictsDirectory
        fields = '__all__'


class BlocksDirectorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BlocksDirectory
        fields = '__all__'


class VillagesDirectorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = VillagesDirectory
        fields = '__all__'
