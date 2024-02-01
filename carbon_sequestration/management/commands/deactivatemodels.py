import sys

from django.core.management.base import BaseCommand, CommandError
from carbon_sequestration.models import CarbonSequestrationModel


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-m', '--models', type=str, required=True)

    def handle(self, *args, **options):
        try:
            models = [model.strip() for model in options['models'].strip().split(',')]
            for model in models:
                carbon_sequestration_model = CarbonSequestrationModel.objects.get(model=model)
                carbon_sequestration_model.is_active = False
                carbon_sequestration_model.save()
        except RuntimeError:
            raise CommandError('Error deactivating models').with_traceback(sys.exception().__traceback__)

        self.stdout.write(
            self.style.SUCCESS('Successfully deactivated models "%s"' % models)
        )