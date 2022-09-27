from django.test import TestCase

from . import models


class TestShop(TestCase):
    def setUp(self) -> None:
        models.Shop.objects.create(
            name="Cejl",
            address="Cejl 55",
            town="Brno",
            phone="0000000",
            open_hours="10:00:00",
            close_hours="19:00:00",
        )

    def test_list(self):
        pass
        # client = Client()
        # response = client.get("shops")

    def test_create(self):
        pass

    def test_retrieve(self):
        pass

    def test_update(self):
        pass

    def test_partial_update(self):
        pass

    def test_destroy(self):
        pass
