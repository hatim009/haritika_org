from django.db import models


class UserBlock(models.Model):
    user = models.ForeignKey('users.User', related_name='assigned_blocks', on_delete=models.CASCADE)
    block = models.ForeignKey('local_directories.BlocksDirectory', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_block'
        unique_together = ('user', 'block',)