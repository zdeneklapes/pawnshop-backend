import pytest
from django.core.management import call_command
from rest_framework.test import APIClient

from authentication.models import User


@pytest.fixture(scope="function")
def user():
    payload = {"email": "super1@a.com", "password": "a"}
    user = User.objects.create_superuser(**payload)
    return user, payload


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture(scope="module")
def load_all_fixtures(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "users.json", "attendants.json", "customers.json", "products.json", "statistics.json")


@pytest.fixture()
def login_client(client, user):
    response = client.post("http://localhost:8000/authentication/token/create/", data=user[1])
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
    return client
