from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.fields import empty
from users.models import User
from users.serializers import UserBlockSerializer, UserProjectSerializer
from django.db import transaction


class UserSerializer(serializers.ModelSerializer):
    blocks = UserBlockSerializer(many=True, source='assigned_blocks')
    projects = UserProjectSerializer(many=True, source='assigned_projects')
    
    class Meta:
        model = User
        exclude = ['password', 'last_updated', 'last_login']
        read_only_fields = ['is_active', 'date_joined']

    """
    There is a bug in rest_framework.serializers.ListSerializer.get_field() where 
        "if html.is_html_input(dictionary):" on line 604
    returns True for non-html input, hence need to override.
    """
    def get_value(self, dictionary):
        return dictionary.get(self.field_name, empty)

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.name = validated_data.get('name', instance.name)
            instance.email = validated_data.get('email', instance.email)
            instance.gender = validated_data.get('gender', instance.gender)
            instance.user_type = validated_data.get('user_type', instance.user_type)
            instance.save()

            if validated_data.get('assigned_blocks'):
                self.fields['blocks'].update(instance, validated_data['assigned_blocks'])
            else:
                raise ValidationError(['Atleast one block should be assigned to the user.'])
            
            if validated_data.get('assigned_projects'):
                self.fields['projects'].update(instance, validated_data['assigned_projects'])
            else:
                raise ValidationError(['Atleast one project should be assigned to the user.'])
            
            return instance
    
    def create(self, validated_data):
        with transaction.atomic():
            assigned_blocks = validated_data.pop('assigned_blocks')
            assigned_projects = validated_data.pop('assigned_projects')
            user = User(**validated_data)
            user.save()
            
            self.fields['blocks'].create(user, assigned_blocks)
            self.fields['blocks'].create(user, assigned_projects)

            return user


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']