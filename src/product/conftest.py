import pytest
from rest_framework.test import APIClient


@pytest.fixture()
def client():
    return APIClient()


# @pytest.fixture(scope='session')
# def django_db_setup(django_db_setup, django_db_blocker):
#     with django_db_blocker.unblock():
#         call_command('loaddata', 'products.json')
