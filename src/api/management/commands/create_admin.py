import os

from django.contrib.auth.models import User
from django.core.management import BaseCommand

from config.settings import ADMINS

# TODO: Not working


class Command(BaseCommand):
    def handle(self, *args, **options):
        if User.objects.all().count() == 0:
            print("Super user already exists. SKIPPING...")
            print("Creating super user...")
            for user in ADMINS:
                admin = User.objects.create_superuser(
                    email=user["email"],
                    username=user["name"],
                    password=user["password"],
                )
                admin.is_super = True
                admin.is_active = True
                admin.is_admin = True
                admin.save()
                print("Super user created!")
        else:
            print("Admin accounts can only be initialized if no Accounts exist")
