from django.test import Client
from rest_framework import status
from rest_framework.test import APITestCase

# from . import models  # TODO: Why does this not working?
from shop.models import Shop  # TODO: Must be like this


class TestShop(APITestCase):
    shop_url = "/shops"

    def setUp(self) -> None:
        Shop.objects.create(
            name="Cejl",
            address="Cejl 55",
            town="Brno",
            phone="0000000",
            open_hours="10:00:00",
            close_hours="19:00:00",
        )

    def test_list(self):
        client = Client()
        response = client.get(f"{TestShop.shop_url}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        client = Client()
        response = client.post(
            f"{TestShop.shop_url}/",
            data={
                "name": "Cejl",
                "address": "Cejl 55",
                "town": "Brno",
                "phone": "0000000",
                "open_hours": "10:00:00",
                "close_hours": "19:00:00",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve(self):
        response = self.client.get(f"{TestShop.shop_url}/1/")
        self.assertEqual(
            response.data,
            {
                "id": 1,
                "name": "Cejl",
                "address": "Cejl 55",
                "town": "Brno",
                "phone": "0000000",
                "open_hours": "10:00:00",
                "close_hours": "19:00:00",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        shop1 = self.client.get(f"{TestShop.shop_url}/1/")
        shop1.data["name"] = "Krenova"
        response = self.client.put(f"{TestShop.shop_url}/1/", data=shop1.data)
        self.assertEqual(
            response.data,
            {
                "id": 1,
                "name": "Krenova",
                "address": "Cejl 55",
                "town": "Brno",
                "phone": "0000000",
                "open_hours": "10:00:00",
                "close_hours": "19:00:00",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update(self):
        response = self.client.patch(
            f"{TestShop.shop_url}/1/", data={"name": "Krenova"}
        )
        self.assertEqual(
            response.data,
            {
                "id": 1,
                "name": "Krenova",
                "address": "Cejl 55",
                "town": "Brno",
                "phone": "0000000",
                "open_hours": "10:00:00",
                "close_hours": "19:00:00",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy(self):
        response = self.client.delete(f"{TestShop.shop_url}/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
