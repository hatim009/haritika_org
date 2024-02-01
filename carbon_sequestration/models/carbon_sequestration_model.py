from django.db import models


class CarbonSequestrationModel(models.Model):
    
    name = models.CharField(max_length=50, primary_key=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'carbon_sequestration_models'