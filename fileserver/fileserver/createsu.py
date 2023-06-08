from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    help = 'Creates a superuser.'

    def handle(self, *args, **options):
        if not User.objects.filter(email=os.environ.get('ADMIN_EMAIL')).exists():
            User.objects.create_superuser(
                username=os.environ.get('ADMIN_EMAIL'),
                password=os.environ.get('ADMIN_PASSWORD')
            )
        print('Superuser has been created.')