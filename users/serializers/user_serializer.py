from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.fields import empty
from users.models import User
from users.serializers import UserBlockSerializer, UserProjectBlockSerializer
from django.db import transaction


class UserSerializer(serializers.ModelSerializer):
    blocks = UserBlockSerializer(many=True, source='assigned_blocks', required=False)
    projects = UserProjectBlockSerializer(many=True, source='assigned_projects', required=False)
    
    class Meta:
        model = User
        exclude = ['last_updated', 'last_login']
        read_only_fields = ['is_active', 'date_joined']

    def get_fields(self, *args, **kwargs):
        fields = super(UserSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get('request')

        if request and getattr(request, 'method', None) != 'POST':
            fields.pop('password')
        elif request:
            fields['password'].write_only = True

        return fields

    """
    There is a bug in rest_framework.serializers.ListSerializer.get_field() where 
        "if html.is_html_input(dictionary):" on line 604
    returns True for non-html input, hence need to override.
    """
    def get_value(self, dictionary):
        return dictionary.get(self.field_name, empty)

    def validate(self, attrs):
        assigned_blocks = attrs.get('assigned_blocks', {}).values()
        assigned_projects = [(project_assignment_info['project'], attrs['assigned_blocks'][block]) for id, project_assignment_info in attrs.get('assigned_projects', {}).items() for block in project_assignment_info['blocks']]
        
        attrs['assigned_blocks'] = assigned_blocks
        attrs['assigned_projects'] = assigned_projects

        return attrs

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.name = validated_data.get('name', instance.name)
            instance.email = validated_data.get('email', instance.email)
            instance.gender = validated_data.get('gender', instance.gender)
            instance.user_type = validated_data.get('user_type', instance.user_type)
            instance.save()

            self.fields['blocks'].update(instance, validated_data['assigned_blocks'])
            self.fields['projects'].update(instance, validated_data['assigned_projects'])
            
            return instance
    
    def create(self, validated_data):
        with transaction.atomic():
            assigned_blocks = validated_data.pop('assigned_blocks')
            assigned_projects = validated_data.pop('assigned_projects')
            password = validated_data.pop('password')
            user = User(**validated_data)
            user.set_password(password)
            user.save()
            
            self.fields['blocks'].create(user, assigned_blocks)
            self.fields['projects'].create(user, assigned_projects)

            return user


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']