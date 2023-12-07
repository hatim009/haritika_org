from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.fields import empty
from users.models import UserBlock
from local_directories.models import BlocksDirectory


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

    def to_representation(self, instance):
        return super().to_representation(instance)['block']
