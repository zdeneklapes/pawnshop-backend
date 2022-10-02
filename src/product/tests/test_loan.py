import os
from pathlib import Path

from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import (
    APIClient,
    APITestCase,
)

from rest_framework_simplejwt.tokens import RefreshToken

from config.settings import BASE_DIR
from authentication.models import User

APP_DIR = Path(__file__).parent.parent
FIXTURES = [
    os.path.join(BASE_DIR, fixture)
    for fixture in [
        "./authentication/fixtures/users.json",
        "./authentication/fixtures/attendants.json",
        "./authentication/fixtures/customers.json",
        "./shop/fixtures/shops.json",
        "./product/fixtures/products.json",
        "./product/fixtures/loans.json",
    ]
]


def api_client():
    user = User.objects.create_superuser(email="aaaa@a.com", password="a", phone_number="+420777666777")  # nosec
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client


class TestLoan(APITestCase):
    fixtures = FIXTURES

    def setUp(self) -> None:
        self.client = api_client()

    # GET: /loans/
    def test_list(self):
        response = self.client.get("/loans/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # POST: /loans/
    def test_create(self):
        response: Response = self.client.post(
            path="/loans/",
            data={
                "user": 1,
                "shop": 1,
                "rate": "4",
                "is_active": True,
                "product": {
                    "product_name": "string",
                    "buy_price": 0,
                    "sell_price": 0,
                    "quantity": 0,
                    "date_extended_deadline": None,
                    "date_end": None,
                },
                "customer": {
                    "person_id_number": "string",
                    "name": "string",
                    "personal_id": "string",
                    "personal_id_expiration_date": "2022-09-30",
                    "residence": "string",
                    "citizenship": "string",
                    "birthplace": "string",
                    "gender": "M",
                },
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # GET /loans/{id}
    def test_retrieve(self):
        response = self.client.get("/loans/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # GET /loans/after-maturity/
    def test_update_customer(self):
        self.assert_(False, "Not Implemented")

    # GET /loans/extend-date/{id}/
    def test_extend_date(self):
        self.assert_(False, "Not Implemented")
