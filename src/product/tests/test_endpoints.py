import pytest
from rest_framework import status
from statistic.models.choices import StatisticDescription
from product.models import ProductStatusOrData, ProductShopData


@pytest.mark.django_db
@pytest.mark.parametrize(
    "path_data, count, exp_status",
    [
        pytest.param("/product/", 9, status.HTTP_200_OK),
        pytest.param(f"/product/?data={ProductStatusOrData.LOAN.name}", 3, status.HTTP_200_OK),
        pytest.param(f"/product/?data={ProductStatusOrData.OFFER.name}", 2, status.HTTP_200_OK),
        pytest.param(f"/product/?data={ProductStatusOrData.AFTER_MATURITY.name}", 2, status.HTTP_200_OK),
        pytest.param(f"/product/?data={ProductShopData.SHOP_STATS.name}", 3, status.HTTP_200_OK),
    ],
)
def test_get(login_client, load_all_fixtures, path_data, count, exp_status):
    response = login_client.get(path=path_data)
    assert response.data.__len__() == count
    assert response.status_code == exp_status


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
    "product_id, operation, payload, exp_status_patch",
    [
        pytest.param(
            1,
            StatisticDescription.LOAN_RETURN.name,
            {"update": StatisticDescription.LOAN_RETURN.name},
            status.HTTP_200_OK,
        ),
        pytest.param(
            6,
            StatisticDescription.LOAN_EXTEND.name,
            {"update": StatisticDescription.LOAN_EXTEND.name},
            status.HTTP_200_OK,
        ),
        pytest.param(
            7,
            StatisticDescription.LOAN_TO_OFFER.name,
            {"update": StatisticDescription.LOAN_TO_OFFER.name, "sell_price": 1200},
            status.HTTP_200_OK,
        ),
        pytest.param(
            4,
            StatisticDescription.OFFER_SELL.name,
            {"update": StatisticDescription.OFFER_SELL.name, "quantity": 1},
            status.HTTP_200_OK,
        ),
        pytest.param(
            4,
            StatisticDescription.OFFER_BUY.name,
            {"update": StatisticDescription.OFFER_BUY.name, "quantity": 1},
            status.HTTP_200_OK,
        ),
    ],
)
def test_update_status(login_client, load_all_fixtures, product_id, operation, payload, exp_status_patch):
    response_update = login_client.patch(path=f"/product/{product_id}/", data=payload, format="json")
    assert response_update.status_code == exp_status_patch


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


@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
@pytest.mark.django_db
@pytest.mark.xfail
def test_loan_response_data_for_product(login_client, load_all_fixtures):
    pass


@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
@pytest.mark.django_db
@pytest.mark.xfail
def test_after_maturity_response_data_for_product(login_client, load_all_fixtures):
    pass


@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
@pytest.mark.django_db
@pytest.mark.xfail
def test_offer_response_data_for_product(login_client, load_all_fixtures):
    pass
