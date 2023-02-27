from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *arg, **options):
        admin_user = get_user_model().objects.filter(
            email="admin@menu.com", is_superuser=True)
        if admin_user.exists():
            self.stdout.write(self.style.SUCCESS(
                'This admin user already exists.'))
        else:
            get_user_model().objects.create_superuser(
                email="admin@menu.com", password="pass1234")
            self.stdout.write(self.style.SUCCESS('Admin user was created.'))
