import sys

from django.core.management.base import BaseCommand, CommandError
from users.models import User


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-ph', '--phone_number', type=str, required=True)
        parser.add_argument('-p', '--password', type=str, required=True)

    def handle(self, *args, **options):
        try:
            phone_number = options['phone_number']
            password = options['password']
            print(phone_number)
            print(password)
            user = User.objects.get(phone_number=phone_number)
            user.set_password(password)
            user.save()
        except RuntimeError:
            raise CommandError('Error resetting password').with_traceback(sys.exception().__traceback__)

        self.stdout.write(
            self.style.SUCCESS('Successfully updated password for user with phone_number "%s"' % phone_number)
        )