import pytest
from django.core.management import call_command


@pytest.fixture(scope="module")
def load_all_fixtures(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "users.json", "attendants.json", "customers.json", "products.json", "statistics.json")
