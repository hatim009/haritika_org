from django.db import models
from django.utils.translation import gettext_lazy as _


class StatesDirectory(models.Model):
    code = models.IntegerField(_('state code'), primary_key=True, unique=True)
    name = models.CharField(_('state name'), max_length=150, unique=True)

    class Meta:
        db_table = 'states_directory'


class DistrictsDirectory(models.Model):
    code = models.IntegerField(_('district code'), primary_key=True, unique=True)
    name = models.CharField(_('district name'), max_length=150)
    state = models.ForeignKey('StatesDirectory', on_delete=models.CASCADE)

    class Meta:
        db_table = 'districts_directory'


class BlocksDirectory(models.Model):
    code = models.IntegerField(_('block code'), primary_key=True, unique=True)
    name = models.CharField(_('block name'), max_length=150)
    district = models.ForeignKey('DistrictsDirectory', on_delete=models.CASCADE)

    class Meta:
        db_table = 'blocks_directory'


class VillagesDirectory(models.Model):
    code = models.IntegerField(_('village code'), primary_key=True, unique=True)
    name = models.CharField(_('village name'), max_length=150)
    block = models.ForeignKey('BlocksDirectory', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'villages_directory'