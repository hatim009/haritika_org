from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.fields import empty
from .models import User, UserBlock
from local_directories.models import BlocksDirectory
from django.db import transaction



class UserBlockListSerializer(serializers.ListSerializer):
    """
    There is a bug in rest_framework.serializers.ListSerializer.get_field() where 
        "if html.is_html_input(dictionary):" on line 604
    returns True for non-html input, hence need to override.
    """
    def get_value(self, dictionary):
        return dictionary.get(self.field_name, empty)

    def validate(self, block_codes):
        valid_blocks = BlocksDirectory.objects.filter(code__in=block_codes)
        valid_block_codes = [block.code for block in valid_blocks]
        invalid_blocks = [block_code for block_code in block_codes if block_code not in valid_block_codes]
        if invalid_blocks:
            raise ValidationError(['Invalid block(s) assigned. Invalid block(s): %s'% (invalid_blocks)])
        return valid_blocks

    def to_internal_value(self, data):
        return [int(block_code.strip()) for block_code in data.strip().split(',')]
    
    def update(self, user, assigned_blocks):
        assigned_block_codes = [block.code for block in assigned_blocks]
        curr_user_blocks = user.assigned_blocks.all()
        curr_assigned_blocks = [user_block.block.code for user_block in curr_user_blocks]
        new_user_blocks = [UserBlock(user=user, block=block) for block in assigned_blocks if block.code not in curr_assigned_blocks]
        removed_user_blocks = [user_block for user_block in curr_user_blocks if user_block.block.code not in assigned_block_codes]

        user_blocks = [user_block for user_block in curr_user_blocks if user_block.block.code in assigned_block_codes]
        if new_user_blocks:
            user_blocks += UserBlock.objects.bulk_create(new_user_blocks)
        
        for user_block in removed_user_blocks:
            user_block.delete()  

        return user_blocks 

    def create(self, user, assigned_blocks):     
        user_blocks = [UserBlock(user=user, block=block) for block in assigned_blocks]
        return UserBlock.objects.bulk_create(user_blocks)


class UserBlockSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserBlock
        depth = 3
        fields = ['block']
        list_serializer_class = UserBlockListSerializer


class UserSerializer(serializers.ModelSerializer):
    blocks = UserBlockSerializer(many=True, source='assigned_blocks')
    
    class Meta:
        model = User
        exclude = ['password', 'last_updated', 'last_login']
        read_only_fields = ['is_active', 'date_joined']

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

        return instance
    
    def create(self, validated_data):
        with transaction.atomic():
            assigned_blocks = validated_data.pop('assigned_blocks')
            user = User(**validated_data)
            user.save()
            if assigned_blocks:
                self.fields['blocks'].create(user, assigned_blocks)

        return user


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']