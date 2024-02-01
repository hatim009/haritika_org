from django.db import models
from django.utils.translation import gettext_lazy as _



class CarbonSequestrationProgress(models.Model):

    carbon_sequestration = models.ForeignKey('carbon_sequestration.CarbonSequestration', related_name='progress', on_delete=models.CASCADE)
    model = models.ForeignKey('carbon_sequestration.CarbonSequestrationModel', related_name='models', on_delete=models.DO_NOTHING)
    total_pits_target = models.IntegerField(default=0)
    total_pits_dug = models.IntegerField(default=0)
    total_pits_fertilized = models.IntegerField(default=0)
    total_pits_planted = models.IntegerField(default=0)

    class Meta:
        db_table = 'carbon_sequestration_progress'
        unique_together = ('carbon_sequestration', 'model')