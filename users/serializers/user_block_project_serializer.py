import json

from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.fields import empty
from users.models import User, UserProjectBlock
from projects.models import Project


class UserProjectBlockListSerializer(serializers.ListSerializer):
    """
    There is a bug in rest_framework.serializers.ListSerializer.get_field() where 
        "if html.is_html_input(dictionary):" on line 604
    returns True for non-html input, hence need to override.
    """
    def get_value(self, dictionary):
        return dictionary.get(self.field_name, empty)

    def validate(self, projects):
        if not projects and self.context['request'].user.user_type != User.UserType.ADMIN:
            raise ValidationError(['At least 1 project must be assigned to the user.'])

        valid_projects_list = Project.objects.filter(is_active=True).filter(id__in=projects.keys())
        valid_projects = {project.id: project for project in valid_projects_list}
        invalid_projects = [project_id for project_id in projects.keys() if project_id not in valid_projects]
        
        if invalid_projects:
            raise ValidationError(['Invalid project(s) assigned. Invalid project(s): %s'% (invalid_projects)])
        
        assigned_blocks = set(json.loads(self.context['request'].data['blocks']))
        invalid_blocks = [block for blocks in projects.values() for block in blocks if block not in assigned_blocks]

        if invalid_blocks:
            raise ValidationError(['Invalid block(s) assigned. Invalid block(s): %s'% (invalid_blocks)])

        return {id: {'project': project, 'blocks': projects[id]} for id, project in valid_projects.items()}

    def to_internal_value(self, data):
        projects = json.loads(data)
        return {int(project): projects[project] for project in projects}
    
    def update(self, user, assigned_projects):
        assigned_project_ids = [project.id for project in assigned_projects]
        curr_user_projects = user.assigned_projects.all()
        curr_assigned_projects = [user_project.project.id for user_project in curr_user_projects]
        new_user_projects = [UserProjectBlock(user=user, project=project) for project in assigned_projects if project.id not in curr_assigned_projects]
        removed_user_projects = [user_project for user_project in curr_user_projects if user_project.project.id not in assigned_project_ids]

        user_projects = [user_project for user_project in curr_user_projects if user_project.project.id in assigned_project_ids]
        if new_user_projects:
            user_projects += UserProjectBlock.objects.bulk_create(new_user_projects)
        
        for user_project in removed_user_projects:
            user_project.delete()  

        return user_projects 

    def create(self, user, assigned_projects):     
        user_projects = [UserProjectBlock(user=user, project=project) for project in assigned_projects]
        return UserProjectBlock.objects.bulk_create(user_projects)


class UserProjectBlockSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProjectBlock
        fields = ['project', 'block']
        list_serializer_class = UserProjectBlockListSerializer

    def to_representation(self, instance):
        return super().to_representation(instance)['project']