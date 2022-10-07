import pytest
from django.core.management import call_command
from rest_framework.test import APIClient

from authentication.models import User


@pytest.fixture(scope="function")
def user():
    user = User.objects.create_superuser(email="super1@a.com", password="a")
    return user


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture(scope="module")
def load_all_fixtures(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "users.json", "attendants.json", "customers.json", "products.json", "statistics.json")


@pytest.fixture()
def login_client(client, user):
    client.credentials(
        HTTP_AUTHORIZATION="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY2MDA3NTc5LCJpYXQiOjE2NjUxNDM1NzksImp0aSI6ImI3ZGJjMmRiMTQ2NTQzMDJhYjA3ZmMyNzY5YjI1OTY2IiwidXNlcl9pZCI6MX0.s2OFNo8vJyt_W6yOXwQcblI_umUSKNvfFfpCOE14dFM"  # noqa: E501
    )
    return client
