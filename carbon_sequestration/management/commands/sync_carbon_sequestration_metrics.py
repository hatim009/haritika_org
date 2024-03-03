import sys

from django.db import transaction
from django.core.management.base import BaseCommand, CommandError
from carbon_sequestration.models import CarbonSequestration


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            carbon_sequestration_list = CarbonSequestration.objects.all()
            for carbon_sequestration in carbon_sequestration_list:
                with transaction.atomic():
                    progress = [model_progress for model_progress in carbon_sequestration.progress.all() if model_progress.model.is_active]

                    carbon_sequestration.total_pits_target = 0
                    carbon_sequestration.total_pits_dug = 0
                    carbon_sequestration.total_pits_fertilized = 0
                    carbon_sequestration.total_pits_planted = 0

                    for model_progress in progress:
                        carbon_sequestration.total_pits_target += model_progress.total_pits_target
                        carbon_sequestration.total_pits_dug += model_progress.total_pits_dug
                        carbon_sequestration.total_pits_fertilized += model_progress.total_pits_fertilized
                        carbon_sequestration.total_pits_planted += model_progress.total_pits_planted

                    carbon_sequestration.save()
        except RuntimeError:
            raise CommandError('Error syncing metrics.').with_traceback(sys.exception().__traceback__)

        self.stdout.write(
            self.style.SUCCESS('Successfully synced metrics.')
        )