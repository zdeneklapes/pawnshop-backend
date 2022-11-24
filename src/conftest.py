import pytest
from django.core.management import call_command
from rest_framework.test import APIClient

from authentication.models import User, AttendantProfile
from config.settings import SIMPLE_JWT

# ######################################################################################################################
# Global Variables
# ######################################################################################################################
FIXTURES = [
    "tests/test_groups.json",
    "tests/test_users.json",
    "tests/test_attendants.json",
    "test_customers.json",
    "test_products.json",
    "test_statistics.json",
]


# ######################################################################################################################
# Data
# ######################################################################################################################
@pytest.fixture(scope="module")
def load_all_scope_module(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", FIXTURES)
        call_command("update_groups_permissions")


@pytest.fixture(scope="function")
def load_all_scope_function(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", FIXTURES)
        call_command("update_groups_permissions")


@pytest.fixture(scope="function")
def load_groups_scope_function(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", FIXTURES)
        call_command("update_groups_permissions")


# ######################################################################################################################
# Users
# ######################################################################################################################
@pytest.fixture(scope="function")
def admin(load_groups_scope_function):
    payload = {"email": "admin_test1@a.com", "password": "admin_test1"}
    user = User.objects.create_user(**payload)
    return user, payload


@pytest.fixture(scope="function")
def attendant(load_groups_scope_function):
    payload = {"email": "atendant_test1@a.com", "password": "attendant_test1"}
    user = AttendantProfile.objects.create_user(**payload)
    return user, payload


# ######################################################################################################################
# Clients
# ######################################################################################################################
@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def client_admin(client, admin):
    response = client.post("http://localhost:8000/authentication/token/create/", data=admin[1])
    client.credentials(HTTP_AUTHORIZATION=f"{SIMPLE_JWT['AUTH_HEADER_TYPES'][0]} {response.data['access']}")
    return client


@pytest.fixture()
def client_attendant(client, attendant):
    response = client.post("http://localhost:8000/authentication/token/create/", data=attendant[1])
    client.credentials(HTTP_AUTHORIZATION=f"{SIMPLE_JWT['AUTH_HEADER_TYPES'][0]} {response.data['access']}")
    return client
