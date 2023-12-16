from django.db import models
from django.core.validators import MinValueValidator


class CarbonSequestration(models.Model):
    land_parcel = models.ForeignKey('land_parcels.LandParcel', on_delete=models.CASCADE)
    carbon_waiver_document = models.ForeignKey('files_manager.File', related_name='carbon_waiver_document', on_delete=models.CASCADE)
    agreement_document_type = models.ForeignKey('files_manager.File', related_name='agreement_document_type', on_delete=models.CASCADE)
    gram_panchayat_resolution = models.ForeignKey('files_manager.File', related_name='gram_panchayat_resolution', on_delete=models.CASCADE)
    total_pits_target = models.IntegerField(validators=[MinValueValidator(1)])
    total_pits_dug = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    total_pits_fertilized = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    total_pits_planted = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    class Meta:
        db_table = 'carbon_sequestration'