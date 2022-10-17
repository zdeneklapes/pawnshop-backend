import pytest
from django.core.management import call_command
from rest_framework.test import APIClient

from authentication.models import User
from config.settings import SIMPLE_JWT


@pytest.fixture(autouse=True)
def test_login_required(settings):
    settings.AUTH = True


@pytest.fixture(autouse=True)
def test_login_not_required(settings):
    settings.AUTH = False


@pytest.fixture(scope="function")
def user():
    payload = {"email": "super1@a.com", "password": "a"}
    user = User.objects.create_superuser(**payload)
    return user, payload


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture(scope="module")
def load_all_fixtures_for_module(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "users.json", "attendants.json", "customers.json", "products.json", "statistics.json")


@pytest.fixture(scope="function")
def load_all_fixtures_for_function(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "users.json", "attendants.json", "customers.json", "products.json", "statistics.json")


@pytest.fixture()
def login_client(client, user, test_login_required):
    response = client.post("http://localhost:8000/authentication/token/create/", data=user[1])
    client.credentials(HTTP_AUTHORIZATION=f"{SIMPLE_JWT['AUTH_HEADER_TYPES'][0]} {response.data['access']}")
    return client
