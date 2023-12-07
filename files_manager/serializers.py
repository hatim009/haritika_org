from rest_framework import serializers
from rest_framework.fields import empty
from .models import File
import json


class FileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = File
        fields = '__all__'

    """
    There is a bug in rest_framework.serializers.ListSerializer.get_field() where 
        "if html.is_html_input(dictionary):" on line 604
    returns True for non-html input, hence need to override.
    """
    def get_value(self, dictionary):
        return dictionary.get(self.field_name, empty)

    def to_internal_value(self, data):
        if isinstance(data, dict):
            return super().to_internal_value(data)
        
        return super().to_internal_value(json.loads(data))

    def bulk_create(self, validated_data):
        files = [File(url=file['url'], hash=file['hash']) for file in validated_data]
        return File.objects.bulk_create(files)
    
    def bulk_update(self, instances, validated_data):
        new_instances = []
        updated_instances = []
        for file in validated_data:
            if file.get('id') and instances.get(file['id']):
                instance = instances.pop(file['id'])
                instance.url = file.get('url', instance.url)
                instance.hash = file.get('hash', instance.hash)

                instance.save()
                updated_instances.append(instance)
            else:
                new_instances.append(File(url=file['url'], hash=file['hash']))

        updated_instances += File.objects.bulk_create(new_instances)

        for id, instance in instances.items():
            instance.delete()

        return updated_instances

        


