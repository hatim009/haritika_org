from rest_framework import serializers
from .models import StatesDirectory, DistrictsDirectory, BlocksDirectory, VillagesDirectory
from rest_framework.fields import empty



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
    
    def __init__(self, instance=None, *args, **kwargs):
        if 'depth' in kwargs:
            self.Meta.depth = kwargs.pop('depth')
            self.Meta.exclude = []
        super().__init__(instance, *args, **kwargs)

    class Meta:
        model = VillagesDirectory
        exclude = ['block']

    """
    There is a bug in rest_framework.serializers.ListSerializer.get_field() where 
        "if html.is_html_input(dictionary):" on line 604
    returns True for non-html input, hence need to override.
    """
    def get_value(self, dictionary):
        return dictionary.get(self.field_name, empty)
    
    def to_internal_value(self, data):
        return VillagesDirectory.objects.get(pk=data)
