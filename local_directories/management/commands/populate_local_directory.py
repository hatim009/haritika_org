import os
import csv
import sys

from django.core.management.base import BaseCommand, CommandError
from local_directories.models import StatesDirectory, DistrictsDirectory, BlocksDirectory, VillagesDirectory


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            base_dir = 'resources/localDirectory/'
            directories = os.listdir(base_dir)
            for directory in directories:
                if directory.endswith('Directory'):
                    with open(base_dir + directory + '/allBlocksAndVillages.csv', 'r') as csv_file:
                        csv_reader = csv.DictReader(csv_file)
                        for row in csv_reader:
                            assert(len(row) == 8)

                            state_directory, state_created = StatesDirectory.objects.get_or_create(code=row['State Code'], name=row['State Name'])
                            print('{0}: {1}\n'.format(state_directory.name, state_created))
                            
                            district_directory, district_created = DistrictsDirectory.objects.get_or_create(code=row['District Code'], name=row['District Name'], state_code=state_directory)
                            print('{0}: {1}\n'.format(district_directory.name, district_created))
                            
                            block_directory, block_created  = BlocksDirectory.objects.get_or_create(code=row['Block Code'], name=row['Block Name'], district_code=district_directory)
                            print('{0}: {1}\n'.format(block_directory.name, block_created))

                            village_directory, village_created = VillagesDirectory.objects.get_or_create(code=row['Village Code'], name=row['Village Name'], block_code=block_directory)
                            print('{0}: {1}\n'.format(village_directory.name, village_created))
                            
        except RuntimeError:
            raise CommandError('Error populating local diretory').with_traceback(sys.exception().__traceback__)

        self.stdout.write(
            self.style.SUCCESS('Successfully populated local directory!!!')
        )