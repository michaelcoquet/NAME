from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        if User.objects.exists():
            return

        username = "admin"
        password = "admin"
        email = "admin"

        User.objects.create_superuser(username=username, password=password, email=email)

        self.stdout.write(f"************************************")
        self.stdout.write(f"Local superuser created successfully\n")
