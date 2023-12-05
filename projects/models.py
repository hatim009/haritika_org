from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=500, unique=True, null=False, blank=False)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'projects'