import datetime

import pytest
from rest_framework import status
from product.models import ProductStatusOrData
from statistic.models import StatisticDescription

from common import utils


@pytest.mark.parametrize(
    "payload, exp_status",
    [
        # OFFER
        pytest.param(
            {
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
# @pytest.mark.xfail  # TODO: Solve conf.settings.AUTH = True settings.AUTH = True
def test_loan_create_calc(client_admin, admin, load_all_fixtures_for_module, payload, exp_status):
    response_update = client_admin.post(path="/product/", data=payload, format="json")
    assert response_update.status_code == exp_status

    if exp_status == status.HTTP_201_CREATED:
        payload["date_create"] = datetime.date.today()
        payload["date_extend"] = datetime.date.today()
        payload["date_end"] = datetime.date.today() + datetime.timedelta(weeks=4)

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
def test_loan_extend_calc(client_admin, load_all_fixtures_for_module, product_id, payload, exp_status):
    response_get = client_admin.get(path=f"/product/{product_id}/", data=payload, format="json")
    response_update = client_admin.patch(path=f"/product/{product_id}/", data=payload, format="json")
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
def test_loan_return_calc(client_admin, load_all_fixtures_for_module, product_id, payload, exp_status):
    response_get = client_admin.get(path=f"/product/{product_id}/", data=payload, format="json")
    response_update = client_admin.patch(path=f"/product/{product_id}/", data=payload, format="json")
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
