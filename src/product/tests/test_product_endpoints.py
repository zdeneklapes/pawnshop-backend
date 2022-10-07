import pytest
from rest_framework import status


@pytest.mark.django_db
def test_product_urls(login_client):
    response = login_client.get(path="/product/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload_data, exp_status_post, exp_status_get",
    [
        pytest.param(
            {
                "user": 1,
                "status": "LOAN",
                "customer": {
                    "full_name": "a b",
                    "residence": "Cejl 2",
                    "sex": "M",
                    "nationality": "CZ",
                    "personal_id": "0000000000",
                    "personal_id_expiration_date": "2022-10-10",
                    "birthplace": "Brno",
                    "id_birth": "000000/0100",
                },
                "interest_rate_or_quantity": 3,
                "inventory_id": 3,
                "product_name": "3",
                "buy_price": 3,
                "sell_price": 5,
            },
            status.HTTP_201_CREATED,
            status.HTTP_200_OK,
        ),
        pytest.param(
            {
                "user": 1,
                "status": "OFFER",
                "customer": {
                    "full_name": "a b",
                    "residence": "Cejl 2",
                    "sex": "M",
                    "nationality": "CZ",
                    "personal_id": "0000000000",
                    "personal_id_expiration_date": "2022-10-10",
                    "birthplace": "Brno",
                    "id_birth": "000000/0100",
                },
                "interest_rate_or_quantity": 3,
                "inventory_id": 3,
                "product_name": "3",
                "buy_price": 3,
                "sell_price": 5,
            },
            status.HTTP_201_CREATED,
            status.HTTP_200_OK,
        ),
        pytest.param(
            {
                "user": 1,
                "status": "AFTER_MATURITY",
                "customer": {
                    "full_name": "a b",
                    "residence": "Cejl 2",
                    "sex": "M",
                    "nationality": "CZ",
                    "personal_id": "0000000000",
                    "personal_id_expiration_date": "2022-10-10",
                    "birthplace": "Brno",
                    "id_birth": "000000/0100",
                },
                "interest_rate_or_quantity": 3,
                "inventory_id": 3,
                "product_name": "3",
                "buy_price": 3,
                "sell_price": 5,
            },
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_404_NOT_FOUND,
            marks=pytest.mark.xfail,
        ),
    ],
)
def test_product_post_get(login_client, payload_data, exp_status_post, exp_status_get):
    response_product_create = login_client.post(path="/product/", data=payload_data, format="json")
    response_product_retrieve = login_client.get(path="/product/1/")
    assert response_product_create.status_code == exp_status_post
    assert response_product_retrieve.status_code == exp_status_get


@pytest.mark.django_db
def test_update_product(login_client, load_all_fixtures):
    response_loans = login_client.get(path="/product/?status=LOAN")
    response_offers = login_client.get(path="/product/?status=OFFER")
    response_after_maturity = login_client.get(path="/product/?status=AFTER_MATURITY")
    response_shop_data = login_client.get(path="/product/?status=SHOP_STATA")
    assert response_loans.status_code == status.HTTP_200_OK
    assert response_offers.status_code == status.HTTP_200_OK
    assert response_after_maturity.status_code == status.HTTP_200_OK
    assert response_shop_data.status_code == status.HTTP_200_OK
