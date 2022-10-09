import pytest
from rest_framework import status
from product.models import ProductStatusOrData
from statistic.models import StatisticDescription


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
def test_is_update_possible(login_client, load_all_fixtures, product_id, payload, exp_status):
    response_update = login_client.patch(path=f"/product/{product_id}/", data=payload, format="json")
    assert response_update.status_code == exp_status


@pytest.mark.parametrize(
    "product_id, payload, exp_status",
    [
        # OFFER
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
    ],
)
@pytest.mark.django_db
def test_offer_buy_sell_calculation_quantity(login_client, load_all_fixtures, product_id, payload, exp_status):
    response_update = login_client.patch(path=f"/product/{product_id}/", data=payload, format="json")
    assert response_update.status_code == exp_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    "path_url, exp_status",
    [
        pytest.param(f"/product/?data={ProductStatusOrData.LOAN.name}", status.HTTP_200_OK),
    ],
)
def test_loan_create(login_client, load_all_fixtures, path_url, exp_status):
    response = login_client.get(path=path_url)
    assert response.status_code == exp_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    "path_url, exp_status",
    [
        pytest.param(f"/product/?data={ProductStatusOrData.LOAN.name}", status.HTTP_200_OK),
    ],
)
def test_loan_update(login_client, load_all_fixtures, path_url, exp_status):
    response = login_client.get(path=path_url)
    assert response.status_code == exp_status


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
def test_update_data(login_client, load_all_fixtures, product_id, payload_data, exp_status_patch, exp_status_get):
    response_update = login_client.patch(path=f"/product/{product_id}/", data=payload_data, format="json")
    response_get = login_client.get(path="/product/1/")
    assert response_update.status_code == exp_status_patch
    assert response_update.status_code == exp_status_get
    assert response_get.data["product_name"] == payload_data["product_name"]
    assert response_get.data["sell_price"] == payload_data["sell_price"]
    assert response_get.data["date_create"] == payload_data["date_create"]
    assert response_get.data["date_extend"] == payload_data["date_extend"]
    assert response_get.data["inventory_id"] == payload_data["inventory_id"]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "path_url, exp_status",
    [
        pytest.param(f"/product/?data={ProductStatusOrData.LOAN.name}", status.HTTP_200_OK),
    ],
)
def test_loan_interest_and_sell_price_response(login_client, load_all_fixtures, path_url, exp_status):
    response = login_client.get(path=path_url)
    assert response.status_code == exp_status

    # for i in response.data:
    #     pass


@pytest.mark.django_db
@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
def test_loan_response_data_for_product(login_client, load_all_fixtures):
    pass


@pytest.mark.django_db
@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
def test_loan_create_calculations(login_client, load_all_fixtures):
    pass


@pytest.mark.django_db
@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
def test_loan_extend_calculations(login_client, load_all_fixtures):
    pass
