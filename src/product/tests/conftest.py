import pytest
from rest_framework.test import APIClient
from authentication.models import User


@pytest.fixture(scope="function")
def user():
    user = User.objects.create_superuser(email="a@a.com", password="a")
    return user


@pytest.fixture()
def client():
    return APIClient()
