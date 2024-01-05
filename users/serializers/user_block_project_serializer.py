import json

from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.fields import empty
from users.models import User, UserProjectBlock
from projects.models import Project
from projects.serializers import ProjectSerializer


class UserProjectBlockListSerializer(serializers.ListSerializer):
    """
    There is a bug in rest_framework.serializers.ListSerializer.get_field() where 
        "if html.is_html_input(dictionary):" on line 604
    returns True for non-html input, hence need to override.
    """
    def get_value(self, dictionary):
        return dictionary.get(self.field_name, empty)

    def validate(self, assigned_projects):
        if not assigned_projects and self.context['request'].user.user_type != User.UserType.ADMIN:
            raise ValidationError(['At least 1 project must be assigned to the user.'])

        valid_projects_list = Project.objects.filter(is_active=True).filter(id__in=assigned_projects.keys())
        valid_projects = {project.id: project for project in valid_projects_list}
        invalid_projects = [project_id for project_id in assigned_projects.keys() if project_id not in valid_projects]
        
        if invalid_projects:
            raise ValidationError(['Invalid project(s) assigned. Invalid project(s): %s'% (invalid_projects)])
        
        assigned_blocks = set(json.loads(self.context['request'].data['blocks']))
        invalid_blocks = [block for blocks in assigned_projects.values() for block in blocks if block not in assigned_blocks]

        if invalid_blocks:
            raise ValidationError(['Invalid block(s) assigned. Invalid block(s): %s'% (invalid_blocks)])

        return {id: {'project': project, 'blocks': assigned_projects[id]} for id, project in valid_projects.items()}

    def to_internal_value(self, data):
        projects = json.loads(data)
        return {int(project): projects[project] for project in projects}
    
    def to_representation(self, data):
        project_block_list = super().to_representation(data)
        project_blocks_map = {}
        for project_block in project_block_list:
            project_id = project_block['project']['id']
            project_name = project_block['project']['name']
            block = project_block['block']
            if project_id not in project_blocks_map:
                project_blocks_map[project_id] = {
                    'name': project_name,
                    'blocks': [block]
                }
            else:
                project_blocks_map[project_id]['blocks'].append(block)

        return project_blocks_map
    
    def update(self, user, project_block_list):
        project_block_map = {"-".join([str(project.id), str(block.code)]): (project, block) for project, block in project_block_list}
        curr_project_blocks = user.assigned_projects.all()
        curr_project_block_ids = ["-".join([str(project_block.project.id), str(project_block.block.code)]) for project_block in curr_project_blocks]
        new_project_blocks = [UserProjectBlock(user=user, project=project_block_map[project_block_id][0], block=project_block_map[project_block_id][1]) for project_block_id in project_block_map if project_block_id not in curr_project_block_ids]
        removed_project_blocks = [project_block for project_block in curr_project_blocks if "-".join([str(project_block.project.id), str(project_block.block.code)]) not in project_block_map]

        project_blocks = [project_block for project_block in curr_project_blocks if "-".join([str(project_block.project.id), str(project_block.block.code)]) in project_block_map]
        if new_project_blocks:
            project_blocks += UserProjectBlock.objects.bulk_create(new_project_blocks)
        
        for project_block in removed_project_blocks:
            project_block.delete()  

        return project_blocks 

    def create(self, user, assigned_projects):     
        user_project_blocks = [UserProjectBlock(user=user, project=project, block=block) for project, block in assigned_projects]
        return UserProjectBlock.objects.bulk_create(user_project_blocks)


class UserProjectBlockSerializer(serializers.ModelSerializer):

    project = ProjectSerializer(read_only=True)

    class Meta:
        model = UserProjectBlock
        fields = ['project', 'block']
        list_serializer_class = UserProjectBlockListSerializer