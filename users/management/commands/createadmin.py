import sys

from django.core.management.base import BaseCommand, CommandError
from users.models import UserManager


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-ph', '--phone_number', type=str, required=True)
        parser.add_argument('-p', '--password', type=str, required=True)
        parser.add_argument('-em', '--email', type=str, required=True)

    def handle(self, *args, **options):
        try:
            phone_number = options['phone_number']
            password = options['password']
            email = options['email']
            UserManager().create_user(phone_number=phone_number, password=password, email=email)
        except RuntimeError:
            raise CommandError('Error creating admin').with_traceback(sys.exception().__traceback__)

        self.stdout.write(
            self.style.SUCCESS('Successfully created admin with phone_number "%s"' % phone_number)
        )