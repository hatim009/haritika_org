import sys

from django.core.management.base import BaseCommand, CommandError
from users.models import UserManager


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument('-u', '--username', type=str, required=True)
        parser.add_argument('-p', '--password', type=str, required=True)

    def handle(self, *args, **options):
        try:
            username = options['username']
            password = options['password']
            UserManager().create_user(username=username, password=password)
        except RuntimeError:
            raise CommandError('Error creating admin').with_traceback(sys.exception().__traceback__)

        self.stdout.write(
            self.style.SUCCESS('Successfully created admin with username "%s"' % username)
        )