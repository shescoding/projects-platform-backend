from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = str(Path('.') / '.env')
load_dotenv(dotenv_path=env_path)


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                os.getenv('SUPERUSER_USERNAME'), os.getenv('SUPERUSER_EMAIL'), os.getenv('SUPERUSER_PASSWORD'))
            self.stdout.write(self.style.SUCCESS(
                'Successfully created new super user'))
