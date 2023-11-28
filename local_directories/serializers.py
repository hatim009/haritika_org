from rest_framework import serializers
from .models import StatesDirectory, DistrictsDirectory, BlocksDirectory, VillagesDirectory


class StatesDirectorySerializer(serializers.ModelSerializer):

    class Meta:
        model = StatesDirectory
        fields = '__all__'


class DistrictsDirectorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DistrictsDirectory
        exclude = ['state']


class BlocksDirectorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BlocksDirectory
        exclude = ['district']


class VillagesDirectorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = VillagesDirectory
        exclude = ['block']
