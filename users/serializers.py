from rest_framework import serializers
from local_directories.serializers import StatesDirectorySerializer, DistrictsDirectorySerializer, BlocksDirectorySerializer
from .models import User, UserBlock


class UserBlockSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserBlock
        depth = 3
        fields = ['block']

    def create(self, validated_data):
        user_block = UserBlock.objects.create(user=validated_data['user'], block=validated_data['block'])
        user_block.save()
        return user_block


class UserSerializer(serializers.ModelSerializer):
    assigned_blocks = UserBlockSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        exclude = ['password', 'last_updated', 'last_login']


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']