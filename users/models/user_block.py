from django.db import models


class UserBlock(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='assigned_blocks')
    block = models.ForeignKey('local_directories.BlocksDirectory', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_block'
        unique_together = ('user', 'block',)