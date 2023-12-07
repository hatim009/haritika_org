from django.db import models


class LandParcelPicture(models.Model):

    land_parcel = models.ForeignKey('land_parcels.LandParcel', related_name='land_parcel_pictures', on_delete=models.CASCADE)
    picture = models.ForeignKey('files_manager.File', on_delete=models.CASCADE)

    class Meta:
        db_table = 'land_parcel_picture'
        unique_together = ('land_parcel', 'picture')