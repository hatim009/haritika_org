from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'last_updated', 'last_login']


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']