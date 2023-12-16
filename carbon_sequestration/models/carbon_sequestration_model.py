from django.db import models
from django.utils.translation import gettext_lazy as _



class CarbonSequestrationModel(models.Model):

    class ProjectModel(models.TextChoices):
        MODEL_1_1 = 'MODEL_1_1', _('Model_1_1')
        MODEL_1_2 = 'MODEL_1_2', _('Model_1_2')
        MODEL_2_1 = 'MODEL_2_1', _('Model_2_1')
        MODEL_2_2 = 'MODEL_2_2', _('Model_2_2')
        MODEL_3 = 'MODEL_3', _('Model_3')
        MODEL_4 = 'MODEL_4', _('Model_4')
    
    carbon_sequestration = models.ForeignKey('carbon_sequestration.CarbonSequestration', related_name='models', on_delete=models.CASCADE)
    model = models.CharField(max_length=20, choices=ProjectModel.choices)
    total_pits_target = models.IntegerField()
    total_pits_dug = models.IntegerField(default=0)
    total_pits_fertilized = models.IntegerField(default=0)
    total_pits_planted = models.IntegerField(default=0)

    class Meta:
        db_table = 'carbon_sequestration_models'