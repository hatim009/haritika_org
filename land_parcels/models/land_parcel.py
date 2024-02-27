from django.db import models
from django.utils.translation import gettext_lazy as _


class LandParcel(models.Model):
    class OwnershipType(models.TextChoices):
        PRIVATE = 'PRIVATE', _('Private')
        COMMUNITY = 'COMMUNITY', _('Community')

    ownership_type = models.CharField(max_length=20, choices=OwnershipType.choices, default=OwnershipType.PRIVATE)
    farmer = models.ForeignKey('farmers.Farmer', related_name='owned_land_parcels', on_delete=models.CASCADE)
    geo_trace = models.TextField()
    area = models.FloatField()
    khasra_number = models.CharField(max_length=100, unique=True)
    farm_workers = models.IntegerField()
    village = models.ForeignKey('local_directories.VillagesDirectory', on_delete=models.DO_NOTHING)
    added_by = models.ForeignKey('users.User', editable=False, related_name='land_parcels_added_by', on_delete=models.DO_NOTHING)
    added_on = models.DateTimeField(auto_now_add=True)
    last_edited_by = models.ForeignKey('users.User', related_name='land_parcels_last_edited_by', on_delete=models.DO_NOTHING)
    last_edited_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'land_parcels'
