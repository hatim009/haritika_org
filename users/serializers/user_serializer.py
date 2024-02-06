from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.fields import empty
from users.models import User
from users.serializers import UserBlockSerializer, UserProjectBlockSerializer
from files_manager.serializers import FileSerializer
from django.db import transaction


class UserSerializer(serializers.ModelSerializer):
    blocks = UserBlockSerializer(many=True, source='assigned_blocks', required=False)
    projects = UserProjectBlockSerializer(many=True, source='assigned_projects', required=False)
    profile_photo = FileSerializer(required=False)

    class Meta:
        model = User
        exclude = ['last_updated', 'last_login']
        read_only_fields = ['is_active', 'date_joined']

    def get_fields(self, *args, **kwargs):
        fields = super(UserSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get('request')

        if not request or  getattr(request, 'method', None) != 'POST':
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
        user_type = None
        if self.context['request'].method in ['PUT', 'PATCH']:
            user_type = self.context['view'].get_object().user_type
        elif self.context['request'].method in ['POST']:
            user_type = self.context['request'].data['user_type']
        else:
            raise ValidationError(['Invalid action %s' % (self.context['request'].method)])
        
        if user_type == User.UserType.ADMIN:
            return attrs

        assigned_blocks = None
        if self.context['request'].method in ['POST']:
            assert 'assigned_blocks' in attrs
            assigned_blocks = attrs['assigned_blocks']
        elif self.context['request'].method in ['PUT', 'PATCH']:
            if 'assigned_blocks' in attrs:
                assigned_blocks = attrs['assigned_blocks']
            else:
                assigned_blocks = {user_block.block.code: user_block.block for user_block in self.context['view'].get_object().assigned_blocks.all()}
        else:
            raise ValidationError(['Invalid action %s' % (self.context['request'].method)])

        if 'assigned_projects' in attrs:
            assigned_projects = []
            for id, project_assignment_info in attrs['assigned_projects'].items():
                for block in project_assignment_info['blocks']:
                    assigned_projects.append((project_assignment_info['project'], assigned_blocks[block]))

            attrs['assigned_projects'] = assigned_projects

        if 'assigned_blocks' in attrs:
            attrs['assigned_blocks'] = attrs['assigned_blocks'].values()

        return attrs

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.name = validated_data.get('name', instance.name)
            instance.email = validated_data.get('email', instance.email)
            instance.gender = validated_data.get('gender', instance.gender)
            instance.user_type = validated_data.get('user_type', instance.user_type)

            if 'profile_photo' in validated_data:
                if instance.profile_photo :
                    instance.profile_photo = self.fields['profile_photo'].update(instance.profile_photo, validated_data['profile_photo'])
                else:
                    instance.profile_photo = self.fields['profile_photo'].create(validated_data['profile_photo'])

            instance.save()

            if 'assigned_blocks' in validated_data:
                self.fields['blocks'].update(instance, validated_data['assigned_blocks'])
            
            if 'assigned_projects' in validated_data:
                self.fields['projects'].update(instance, validated_data['assigned_projects'])
            
            return instance
    
    def create(self, validated_data):
        with transaction.atomic():
            assigned_blocks = validated_data.pop('assigned_blocks')
            assigned_projects = validated_data.pop('assigned_projects')
            password = validated_data.pop('password')

            if 'profile_photo' in validated_data:
                validated_data['profile_photo'] = self.fields['profile_photo'].create(validated_data['profile_photo'])

            user = User(**validated_data)
            user.set_password(password)
            user.save()
            
            if assigned_blocks:
                self.fields['blocks'].create(user, assigned_blocks)
            
            if assigned_projects:
                self.fields['projects'].create(user, assigned_projects)
            
            return user


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']