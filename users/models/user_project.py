from django.db import models


class UserProject(models.Model):
    user = models.ForeignKey('users.User', related_name='assigned_projects', on_delete=models.CASCADE)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_project'
        unique_together = ('user', 'project',)