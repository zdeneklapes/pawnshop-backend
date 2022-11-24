import datetime

import pytest
from rest_framework import status
from product.models import ProductStatusOrData
from statistic.models import StatisticDescription


@pytest.mark.parametrize(
    "payload, exp_status",
    [
        # OFFER
        pytest.param(
            {
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
# @pytest.mark.xfail  # TODO: Solve conf.settings.AUTH = True settings.AUTH = True
def test_offer_create_calc(client_admin, admin, load_all_scope_module, payload, exp_status):
    response_update = client_admin.post(path="/product/", data=payload, format="json")
    assert response_update.status_code == exp_status

    if exp_status == status.HTTP_201_CREATED:
        payload["date_create"] = datetime.date.today()
        payload["date_extend"] = datetime.date.today()
        payload["date_end"] = None

        assert admin[0].id == response_update.data["user"]
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
    ],
)
@pytest.mark.django_db
def test_offer_update_quantity_calculations(
    client_admin, load_all_scope_function, product_id, payload, exp_offer_status, exp_quantity, exp_status
):
    response_update = client_admin.patch(path=f"/product/{product_id}/", data=payload, format="json")
    assert not response_update.data["interest_rate_or_quantity"].isdecimal()
    assert response_update.data["interest_rate_or_quantity"] == exp_quantity
    assert response_update.data["status"] == exp_offer_status


@pytest.mark.parametrize(
    "product_id, payload, exp_offer_status, exp_quantity, exp_status",
    [
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
def test_offer_update_quantity_calculations_fail(
    client_admin, load_all_scope_function, product_id, payload, exp_offer_status, exp_quantity, exp_status
):
    response_update = client_admin.patch(path=f"/product/{product_id}/", data=payload, format="json")
    assert response_update.status_code == exp_status
