import pytest
from rest_framework.test import APIClient
from authentication.models import User
from django.core.management import call_command


@pytest.fixture(scope="function")
def user():
    user = User.objects.create_superuser(email="a@a.com", password="a")
    return user


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture(scope="session")
def load_fixtures(django_db_setup, django_db_blocker):
    print("fixtures installing...")
    with django_db_blocker.unblock():
        call_command("loaddata", "users.json", "attendants.json", "customers.json", "products.json", "statistics.json")
