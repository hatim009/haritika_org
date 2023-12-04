from django.db import models
from django.core.validators import MinLengthValidator



class File(models.Model):
    url = models.TextField(unique=True)
    hash = models.CharField(max_length=64, validators=[MinLengthValidator(64)], unique=True)

    class Meta:
        db_table = 'files'
