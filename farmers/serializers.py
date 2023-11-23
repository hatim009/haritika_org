from rest_framework import serializers
from .models import Farmer


class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = '__all__'
        read_only_fields = ['added_by', 'added_on', 'last_edited_by', 'last_edited_on']
