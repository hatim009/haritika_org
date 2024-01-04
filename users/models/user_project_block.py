from django.db import models


class UserProjectBlock(models.Model):
    user = models.ForeignKey('users.User', related_name='assigned_projects', on_delete=models.CASCADE)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE)
    block = models.ForeignKey('local_directories.BlocksDirectory', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_project_block'