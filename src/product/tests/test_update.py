import pytest
from rest_framework import status

from statistic.models import StatisticDescription
from product.models import ProductStatusOrData


@pytest.mark.parametrize(
    "product_id, payload, response_status",
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
def test_is_update_possible(client_admin, load_all_scope_module, product_id, payload, response_status):
    response_update = client_admin.patch(path=f"/product/{product_id}/", data=payload, format="json")
    assert response_update.status_code == response_status


@pytest.mark.parametrize(
    "product_id, payload, product_status, response_status",
    [
        # OFFER
        pytest.param(
            4,
            {"update": StatisticDescription.OFFER_SELL.name, "quantity": 1},
            ProductStatusOrData.INACTIVE_OFFER.name,
            status.HTTP_200_OK,
        ),
        pytest.param(
            5,
            {"update": StatisticDescription.OFFER_SELL.name, "quantity": 2},
            ProductStatusOrData.INACTIVE_OFFER.name,
            status.HTTP_200_OK,
        ),
    ],
)
@pytest.mark.django_db
def test_offer_sell_quantity_status(
    client_admin, load_all_scope_module, product_id, payload, product_status, response_status
):
    response_update = client_admin.patch(path=f"/product/{product_id}/", data=payload, format="json")
    assert response_update.status_code == response_status
    assert response_update.data["status"] == product_status
