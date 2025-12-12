from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction


class Command(BaseCommand):
    help = 'Create a superuser if it does not exist'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='admin')
        parser.add_argument('--email', type=str, default='admin@example.com')
        parser.add_argument('--password', type=str, default='Admin1234')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        User = get_user_model()

        with transaction.atomic():
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'Superuser "{username}" already exists')
                )
                return

            try:
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Superuser "{username}" created successfully')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Failed to create superuser: {e}')
                )
