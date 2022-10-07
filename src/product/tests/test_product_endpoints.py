import pytest
from rest_framework import status


@pytest.mark.django_db
def test_get(login_client):
    response_all = login_client.get(path="/product/")
    response_loans = login_client.get(path="/product/?status=LOAN")
    response_offers = login_client.get(path="/product/?status=OFFER")
    response_after_maturity = login_client.get(path="/product/?status=AFTER_MATURITY")
    response_shop_data = login_client.get(path="/product/?status=SHOP_STATA")

    assert response_all.status_code == status.HTTP_200_OK
    assert response_loans.status_code == status.HTTP_200_OK
    assert response_offers.status_code == status.HTTP_200_OK
    assert response_after_maturity.status_code == status.HTTP_200_OK
    assert response_shop_data.status_code == status.HTTP_200_OK


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
def test_post_get(login_client, payload_data, exp_status_post, exp_status_get):
    response_product_create = login_client.post(path="/product/", data=payload_data, format="json")
    response_product_retrieve = login_client.get(path="/product/1/")
    assert response_product_create.status_code == exp_status_post
    assert response_product_retrieve.status_code == exp_status_get


@pytest.mark.django_db
@pytest.mark.parametrize(
    "product_id, payload_data, exp_status_patch, exp_status_get",
    [
        pytest.param(
            1,
            {
                "product_name": "Telefon Samsung 1",
                "sell_price": 100,
                "date_create": "2022-09-01T14:31:47.080000Z",
                "date_extend": "2022-09-01T14:31:47.080000Z",
                "inventory_id": 23,
            },
            status.HTTP_200_OK,
            status.HTTP_200_OK,
        ),
    ],
)
def test_update_product(login_client, load_all_fixtures, product_id, payload_data, exp_status_patch, exp_status_get):
    response_update = login_client.patch(
        path=f"/product/{product_id}/?operation=UPDATE", data=payload_data, format="json"
    )
    response_get = login_client.get(path="/product/1/")
    assert response_update.status_code == exp_status_patch
    assert response_update.status_code == exp_status_get
    assert response_get.data["product_name"] == payload_data["product_name"]
    assert response_get.data["sell_price"] == payload_data["sell_price"]
    assert response_get.data["date_create"] == payload_data["date_create"]
    assert response_get.data["date_extend"] == payload_data["date_extend"]
    assert response_get.data["inventory_id"] == payload_data["inventory_id"]


def test_extend(login_client, load_all_fixtures, product_id, payload_data, exp_status_patch, exp_status_get):
    pass


def test_return(login_client, load_all_fixtures, product_id, payload_data, exp_status_patch, exp_status_get):
    pass


def test_loan_to_move(login_client, load_all_fixtures, product_id, payload_data, exp_status_patch, exp_status_get):
    pass


def test_extend(login_client, load_all_fixtures, product_id, payload_data, exp_status_patch, exp_status_get):
    pass


def test_extend(login_client, load_all_fixtures, product_id, payload_data, exp_status_patch, exp_status_get):
    pass
