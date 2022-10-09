import datetime

import pytest
from rest_framework import status
from product.models import ProductStatusOrData
from statistic.models import StatisticDescription
from common import utils


@pytest.mark.parametrize(
    "product_id, payload, exp_status",
    [
        # LOAN
        pytest.param(
            1,
            {"update": StatisticDescription.LOAN_RETURN.name},
            status.HTTP_200_OK,
        ),
        pytest.param(
            1,
            {"update": StatisticDescription.LOAN_EXTEND.name},
            status.HTTP_200_OK,
        ),
        pytest.param(
            1,
            {"update": StatisticDescription.LOAN_TO_OFFER.name, "sell_price": 1200},
            status.HTTP_400_BAD_REQUEST,
        ),
        pytest.param(
            1,
            {"update": StatisticDescription.OFFER_BUY.name, "quantity": 10},
            status.HTTP_400_BAD_REQUEST,
        ),
        pytest.param(
            1,
            {"update": StatisticDescription.OFFER_SELL.name, "quantity": 10},
            status.HTTP_400_BAD_REQUEST,
        ),
        # AFTER_MATURITY
        pytest.param(
            6,
            {"update": StatisticDescription.LOAN_RETURN.name, "quantity": 1},
            status.HTTP_200_OK,
        ),
        pytest.param(
            6,
            {"update": StatisticDescription.LOAN_EXTEND.name, "quantity": 1},
            status.HTTP_200_OK,
        ),
        pytest.param(
            6,
            {"update": StatisticDescription.LOAN_TO_OFFER.name, "sell_price": 1200},
            status.HTTP_200_OK,
        ),
        pytest.param(
            6,
            {"update": StatisticDescription.OFFER_BUY.name, "quantity": 1},
            status.HTTP_400_BAD_REQUEST,
        ),
        pytest.param(
            6,
            {"update": StatisticDescription.OFFER_SELL.name, "quantity": 1},
            status.HTTP_400_BAD_REQUEST,
        ),
        # OFFER
        pytest.param(
            4,
            {"update": StatisticDescription.LOAN_RETURN.name, "quantity": 1},
            status.HTTP_400_BAD_REQUEST,
        ),
        pytest.param(
            4,
            {"update": StatisticDescription.LOAN_EXTEND.name, "quantity": 1},
            status.HTTP_400_BAD_REQUEST,
        ),
        pytest.param(
            4,
            {"update": StatisticDescription.LOAN_TO_OFFER.name, "sell_price": 1200},
            status.HTTP_400_BAD_REQUEST,
        ),
        pytest.param(
            4,
            {"update": StatisticDescription.OFFER_BUY.name, "quantity": 2},
            status.HTTP_200_OK,
        ),
        pytest.param(
            4,
            {"update": StatisticDescription.OFFER_SELL.name, "quantity": 1},
            status.HTTP_200_OK,
        ),
        pytest.param(
            4,
            {"update": StatisticDescription.OFFER_SELL.name, "quantity": 3},
            status.HTTP_400_BAD_REQUEST,
        ),
    ],
)
@pytest.mark.django_db
def test_is_update_possible(login_client, load_all_fixtures_for_module, product_id, payload, exp_status):
    response_update = login_client.patch(path=f"/product/{product_id}/", data=payload, format="json")
    assert response_update.status_code == exp_status


@pytest.mark.parametrize(
    "payload, exp_status",
    [
        # OFFER
        pytest.param(
            {
                "user": 1,
                "status": "OFFER",
                "customer": {
                    "full_name": "a b",
                    "residence": "Cejl 222",
                    "sex": "F",
                    "nationality": "SK",
                    "personal_id": "0000000000",
                    "personal_id_expiration_date": "2023-02-02",
                    "birthplace": "Prha",
                    "id_birth": "000000/0001",
                },
                "interest_rate_or_quantity": "1.0",
                "inventory_id": 3,
                "product_name": "prod1",
                "buy_price": 100,
                "sell_price": 200,
            },
            status.HTTP_201_CREATED,
        ),
        pytest.param(
            {
                "user": 1,
                "status": "OFFER",
                "customer": {
                    "full_name": "a b",
                    "residence": "Cejl 222",
                    "sex": "F",
                    "nationality": "SK",
                    "personal_id": "0000000000",
                    "personal_id_expiration_date": "2023-02-02",
                    "birthplace": "Prha",
                    "id_birth": "000000/0001",
                },
                "interest_rate_or_quantity": "1.5",
                "inventory_id": 3,
                "product_name": "prod2",
                "buy_price": 150,
                "sell_price": 200,
            },
            status.HTTP_400_BAD_REQUEST,
        ),
    ],
)
@pytest.mark.django_db
def test_offer_create_calc(login_client, load_all_fixtures_for_module, payload, exp_status):
    response_update = login_client.post(path="/product/", data=payload, format="json")
    assert response_update.status_code == exp_status

    if exp_status == status.HTTP_201_CREATED:
        payload["date_create"] = datetime.date.today()
        payload["date_extend"] = datetime.date.today()
        payload["date_end"] = None

        assert payload["user"] == response_update.data["user"]
        assert payload["status"] == response_update.data["status"]
        assert payload["customer"] == response_update.data["customer"]
        assert payload["interest_rate_or_quantity"] == response_update.data["interest_rate_or_quantity"]
        assert payload["inventory_id"] == response_update.data["inventory_id"]
        assert payload["product_name"] == response_update.data["product_name"]
        assert payload["buy_price"] == response_update.data["buy_price"]
        assert payload["sell_price"] == response_update.data["sell_price"]
        assert str(payload["date_create"]) in response_update.data["date_create"]
        assert str(payload["date_extend"]) in response_update.data["date_extend"]
        assert payload["date_end"] == response_update.data["date_end"]


@pytest.mark.parametrize(
    "product_id, payload, exp_offer_status, exp_quantity, exp_status",
    [
        # OFFER
        pytest.param(
            4,
            {"update": StatisticDescription.OFFER_BUY.name, "quantity": 2},
            ProductStatusOrData.OFFER.name,
            "3.0",
            status.HTTP_200_OK,
        ),
        pytest.param(
            4,
            {"update": StatisticDescription.OFFER_SELL.name, "quantity": 1},
            ProductStatusOrData.INACTIVE_OFFER.name,
            "0.0",
            status.HTTP_200_OK,
        ),
        pytest.param(
            4,
            {"update": StatisticDescription.OFFER_SELL.name, "quantity": 3},
            ProductStatusOrData.OFFER.name,
            "0.0",
            status.HTTP_400_BAD_REQUEST,
        ),
    ],
)
@pytest.mark.django_db
def test_offer_update_quantity_calculations(
    login_client, load_all_fixtures_for_function, product_id, payload, exp_offer_status, exp_quantity, exp_status
):
    response_update = login_client.patch(path=f"/product/{product_id}/", data=payload, format="json")

    if exp_status == status.HTTP_200_OK:
        assert not response_update.data["interest_rate_or_quantity"].isdecimal()
        assert response_update.data["interest_rate_or_quantity"] == exp_quantity
        assert response_update.data["status"] == exp_offer_status

    assert response_update.status_code == exp_status


@pytest.mark.parametrize(
    "payload, exp_status",
    [
        # OFFER
        pytest.param(
            {
                "user": 1,
                "status": "LOAN",
                "customer": {
                    "full_name": "a b",
                    "residence": "Cejl 222",
                    "sex": "F",
                    "nationality": "SK",
                    "personal_id": "0000000000",
                    "personal_id_expiration_date": "2023-02-02",
                    "birthplace": "Prha",
                    "id_birth": "000000/0001",
                },
                "interest_rate_or_quantity": "3.0",
                "inventory_id": 3,
                "product_name": "prod1",
                "buy_price": 11000,
                "sell_price": 11330,
            },
            status.HTTP_201_CREATED,
        ),
        pytest.param(
            {
                "user": 1,
                "status": "LOAN",
                "customer": {
                    "full_name": "a b",
                    "residence": "Cejl 222",
                    "sex": "F",
                    "nationality": "SK",
                    "personal_id": "0000000000",
                    "personal_id_expiration_date": "2023-02-02",
                    "birthplace": "Prha",
                    "id_birth": "000000/0001",
                },
                "interest_rate_or_quantity": "2.5",
                "inventory_id": 3,
                "product_name": "prod2",
                "buy_price": 150,
                "sell_price": 155,
            },
            status.HTTP_201_CREATED,
        ),
    ],
)
@pytest.mark.django_db
def test_loan_create_calc(login_client, load_all_fixtures_for_module, payload, exp_status):
    response_update = login_client.post(path="/product/", data=payload, format="json")
    assert response_update.status_code == exp_status

    if exp_status == status.HTTP_201_CREATED:
        payload["date_create"] = datetime.date.today()
        payload["date_extend"] = datetime.date.today()
        payload["date_end"] = datetime.date.today() + datetime.timedelta(weeks=4)

        assert payload["user"] == response_update.data["user"]
        assert payload["status"] == response_update.data["status"]
        assert payload["customer"] == response_update.data["customer"]
        assert payload["interest_rate_or_quantity"] == response_update.data["interest_rate_or_quantity"]
        assert payload["inventory_id"] == response_update.data["inventory_id"]
        assert payload["product_name"] == response_update.data["product_name"]
        assert payload["buy_price"] == response_update.data["buy_price"]
        assert payload["sell_price"] == response_update.data["sell_price"]
        assert str(payload["date_create"]) in response_update.data["date_create"]
        assert str(payload["date_extend"]) in response_update.data["date_extend"]
        assert str(payload["date_end"]) in response_update.data["date_end"]


@pytest.mark.parametrize(
    "product_id, payload, exp_status",
    [
        pytest.param(
            1,
            {"update": StatisticDescription.LOAN_EXTEND.name},
            status.HTTP_200_OK,
        )
    ],
)
@pytest.mark.django_db
def test_loan_extend_calc(login_client, load_all_fixtures_for_module, product_id, payload, exp_status):
    response_get = login_client.get(path=f"/product/{product_id}/", data=payload, format="json")
    response_update = login_client.patch(path=f"/product/{product_id}/", data=payload, format="json")
    assert response_update.status_code == exp_status

    # Check update
    if exp_status == status.HTTP_200_OK:
        assert response_get.data["user"] == response_update.data["user"]
        assert response_get.data["status"] == response_update.data["status"] == ProductStatusOrData.LOAN.name
        assert response_get.data["customer"]["id_birth"] == response_update.data["customer"]
        assert response_get.data["interest_rate_or_quantity"] == response_update.data["interest_rate_or_quantity"]
        assert response_get.data["inventory_id"] == response_update.data["inventory_id"]
        assert response_get.data["product_name"] == response_update.data["product_name"]
        assert response_get.data["buy_price"] == response_update.data["buy_price"]
        assert response_get.data["sell_price"] == response_update.data["sell_price"]
        assert str(response_get.data["date_create"]) in response_update.data["date_create"]
        assert str(datetime.date.today()) in response_update.data["date_extend"]
        assert str(datetime.date.today() + datetime.timedelta(weeks=4)) in response_update.data["date_end"]
        assert (
            utils.get_interests(
                rate=float(response_get.data["interest_rate_or_quantity"]),
                buy_price=response_get.data["buy_price"],
                from_date=datetime.date.today(),
            )
            == response_update.data["interest"]
        )


@pytest.mark.parametrize(
    "product_id, payload, exp_status",
    [
        pytest.param(
            1,
            {"update": StatisticDescription.LOAN_RETURN.name},
            status.HTTP_200_OK,
        )
    ],
)
@pytest.mark.django_db
def test_loan_return_calc(login_client, load_all_fixtures_for_module, product_id, payload, exp_status):
    response_get = login_client.get(path=f"/product/{product_id}/", data=payload, format="json")
    response_update = login_client.patch(path=f"/product/{product_id}/", data=payload, format="json")
    assert response_update.status_code == exp_status

    # Check update
    if exp_status == status.HTTP_200_OK:
        assert response_get.data["user"] == response_update.data["user"]
        assert ProductStatusOrData.INACTIVE_LOAN.name == response_update.data["status"]
        assert response_get.data["customer"]["id_birth"] == response_update.data["customer"]
        assert response_get.data["interest_rate_or_quantity"] == response_update.data["interest_rate_or_quantity"]
        assert response_get.data["inventory_id"] == response_update.data["inventory_id"]
        assert response_get.data["product_name"] == response_update.data["product_name"]
        assert response_get.data["buy_price"] == response_update.data["buy_price"]
        assert response_get.data["sell_price"] == response_update.data["sell_price"]
        assert str(response_get.data["date_create"]) in response_update.data["date_create"]
        assert str(response_get.data["date_extend"]) in response_update.data["date_extend"]
        assert str(datetime.date.today()) in response_update.data["date_end"]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "product_id, payload_data, exp_status_patch, exp_status_get",
    [
        pytest.param(
            1,
            {
                "update": f"{StatisticDescription.UPDATE_DATA.name}",
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
def test_update_data(
    login_client, load_all_fixtures_for_module, product_id, payload_data, exp_status_patch, exp_status_get
):
    response_update = login_client.patch(path=f"/product/{product_id}/", data=payload_data, format="json")
    response_get = login_client.get(path="/product/1/")
    assert response_update.status_code == exp_status_patch
    assert response_update.status_code == exp_status_get
    assert response_get.data["product_name"] == payload_data["product_name"]
    assert response_get.data["sell_price"] == payload_data["sell_price"]
    assert response_get.data["date_create"] == payload_data["date_create"]
    assert response_get.data["date_extend"] == payload_data["date_extend"]
    assert response_get.data["inventory_id"] == payload_data["inventory_id"]
