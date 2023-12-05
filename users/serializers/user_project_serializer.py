from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.fields import empty
from users.models import UserProject
from projects.models import Project


class UserProjectListSerializer(serializers.ListSerializer):
    """
    There is a bug in rest_framework.serializers.ListSerializer.get_field() where 
        "if html.is_html_input(dictionary):" on line 604
    returns True for non-html input, hence need to override.
    """
    def get_value(self, dictionary):
        return dictionary.get(self.field_name, empty)

    def validate(self, project_ids):
        valid_projects = Project.objects.filter(id__in=project_ids)
        valid_project_ids = [project.id for project in valid_projects]
        invalid_projects = [project_id for project_id in project_ids if project_id not in valid_project_ids]
        if invalid_projects:
            raise ValidationError(['Invalid project(s) assigned. Invalid project(s): %s'% (invalid_projects)])
        return valid_projects

    def to_internal_value(self, data):
        return [int(project_id.strip()) for project_id in data.strip().split(',')]
    
    def update(self, user, assigned_projects):
        assigned_project_ids = [project.id for project in assigned_projects]
        curr_user_projects = user.assigned_projects.all()
        curr_assigned_projects = [user_project.project.id for user_project in curr_user_projects]
        new_user_projects = [UserProject(user=user, project=project) for project in assigned_projects if project.id not in curr_assigned_projects]
        removed_user_projects = [user_project for user_project in curr_user_projects if user_project.project.id not in assigned_project_ids]

        user_projects = [user_project for user_project in curr_user_projects if user_project.project.id in assigned_project_ids]
        if new_user_projects:
            user_projects += UserProject.objects.bulk_create(new_user_projects)
        
        for user_project in removed_user_projects:
            user_project.delete()  

        return user_projects 

    def create(self, user, assigned_projects):     
        user_projects = [UserProject(user=user, project=project) for project in assigned_projects]
        return UserProject.objects.bulk_create(user_projects)


class UserProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProject
        fields = ['project']
        depth = 2
        list_serializer_class = UserProjectListSerializer