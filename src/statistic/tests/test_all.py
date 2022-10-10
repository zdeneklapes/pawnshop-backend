import datetime

import pytest
from statistic.models import StatisticDescription, StatisticQPData
from rest_framework import status


@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
@pytest.mark.django_db
@pytest.mark.xfail
def test_loan_create(login_client):
    assert False


@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
@pytest.mark.django_db
@pytest.mark.xfail
def test_loan_extend(login_client):
    assert False


@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
@pytest.mark.django_db
@pytest.mark.xfail
def test_loan_return(login_client):
    assert False


@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
@pytest.mark.django_db
@pytest.mark.xfail
def test_after_maturity_return(login_client):
    assert False


@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
@pytest.mark.django_db
@pytest.mark.xfail
def test_after_maturity_extend(login_client):
    assert False


@pytest.mark.parametrize(
    "product_id, payload_data, exp_status",
    [
        pytest.param(
            4,
            {
                "update": f"{StatisticDescription.OFFER_BUY.name}",
                "quantity": 1,
            },
            status.HTTP_200_OK,
        ),
        pytest.param(
            5,
            {
                "update": f"{StatisticDescription.OFFER_BUY.name}",
                "quantity": 2,
            },
            status.HTTP_200_OK,
        ),
    ],
)
@pytest.mark.django_db
def test_offer_create(login_client, load_all_fixtures_for_function, product_id, payload_data, exp_status):
    response_get = login_client.get(path="/statistic/")
    response_update = login_client.patch(path=f"/product/{product_id}/", data=payload_data, format="json")
    response_get_2 = login_client.get(path="/statistic/")

    product = response_update.data
    old_stat = response_get.data[-1]
    new_stat = response_get_2.data[-1]

    assert len(response_get.data) == len(response_get_2.data) - 1
    assert new_stat["amount"] == old_stat["amount"] - (payload_data["quantity"] * product["buy_price"])
    assert new_stat["profit"] == old_stat["profit"] - (payload_data["quantity"] * product["buy_price"])
    assert str(datetime.date.today()) in new_stat["datetime"]
    assert new_stat["description"] == StatisticDescription.OFFER_BUY.name
    assert new_stat["price"] == -product["buy_price"] * payload_data["quantity"]
    assert new_stat["product"] == product_id


@pytest.mark.parametrize(
    "product_id, payload_data, exp_status",
    [
        pytest.param(
            4,
            {
                "update": f"{StatisticDescription.OFFER_BUY.name}",
                "quantity": 1,
            },
            status.HTTP_200_OK,
        ),
        pytest.param(
            5,
            {
                "update": f"{StatisticDescription.OFFER_BUY.name}",
                "quantity": 2,
            },
            status.HTTP_200_OK,
        ),
    ],
)
@pytest.mark.django_db
def test_offer_buy(login_client, load_all_fixtures_for_function, product_id, payload_data, exp_status):
    response_get = login_client.get(path="/statistic/")
    response_update = login_client.patch(path=f"/product/{product_id}/", data=payload_data, format="json")
    response_get_2 = login_client.get(path="/statistic/")

    product = response_update.data
    old_stat = response_get.data[-1]
    new_stat = response_get_2.data[-1]

    assert len(response_get.data) == len(response_get_2.data) - 1
    assert new_stat["amount"] == old_stat["amount"] - (payload_data["quantity"] * product["buy_price"])
    assert new_stat["profit"] == old_stat["profit"] - (payload_data["quantity"] * product["buy_price"])
    assert str(datetime.date.today()) in new_stat["datetime"]
    assert new_stat["description"] == StatisticDescription.OFFER_BUY.name
    assert new_stat["price"] == -product["buy_price"] * payload_data["quantity"]
    assert new_stat["product"] == product_id


@pytest.mark.parametrize(
    "product_id, payload_data, exp_status",
    [
        pytest.param(
            4,
            {
                "update": f"{StatisticDescription.OFFER_SELL.name}",
                "quantity": 1,
            },
            status.HTTP_200_OK,
        ),
        pytest.param(
            5,
            {
                "update": f"{StatisticDescription.OFFER_SELL.name}",
                "quantity": 2,
            },
            status.HTTP_200_OK,
        ),
    ],
)
@pytest.mark.django_db
def test_offer_sell(login_client, load_all_fixtures_for_function, product_id, payload_data, exp_status):
    response_get = login_client.get(path="/statistic/")
    response_update = login_client.patch(path=f"/product/{product_id}/", data=payload_data, format="json")
    response_get_2 = login_client.get(path="/statistic/")

    product = response_update.data
    old_stat = response_get.data[-1]
    new_stat = response_get_2.data[-1]

    assert len(response_get.data) == len(response_get_2.data) - 1
    assert new_stat["description"] == StatisticDescription.OFFER_SELL.name
    assert new_stat["amount"] == old_stat["amount"] + (payload_data["quantity"] * product["sell_price"])
    assert new_stat["profit"] == old_stat["profit"] + (payload_data["quantity"] * product["sell_price"])
    assert str(datetime.date.today()) in new_stat["datetime"]
    assert new_stat["description"] == StatisticDescription.OFFER_SELL.name
    assert new_stat["price"] == product["sell_price"] * payload_data["quantity"]
    assert new_stat["product"] == product_id


@pytest.mark.parametrize(
    "product_id, payload_data, exp_status",
    [
        pytest.param(
            4,
            {
                "update": f"{StatisticDescription.UPDATE_DATA.name}",
                "product_name": "Telefon Samsung 1",
                "sell_price": 100,
                "date_create": "2022-09-01T14:31:47.080000Z",
                "date_extend": "2022-09-01T14:31:47.080000Z",
                "inventory_id": 23,
            },
            status.HTTP_200_OK,
        ),
    ],
)
@pytest.mark.django_db
def test_offer_update_not_in_db(login_client, load_all_fixtures_for_function, product_id, payload_data, exp_status):
    response_get = login_client.get(path="/statistic/")
    response_get_2 = login_client.get(path="/statistic/")

    old_stat = response_get.data[-1]
    new_stat = response_get_2.data[-1]

    assert len(response_get.data) == len(response_get_2.data)
    assert new_stat["amount"] == old_stat["amount"]
    assert new_stat["profit"] == old_stat["profit"]
    assert new_stat["datetime"] == old_stat["datetime"]
    assert new_stat["description"] == old_stat["description"]
    assert new_stat["price"] == old_stat["price"]
    assert new_stat["product"] == old_stat["product"]


# Data
@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
@pytest.mark.django_db
def test_statistic_default_data(login_client, load_all_fixtures_for_function):
    response_get = login_client.get(path="/statistic/")
    assert len(response_get.data) == 18


@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
@pytest.mark.django_db
def test_statistic_cash_amount_data(login_client, load_all_fixtures_for_function):
    response_get = login_client.get(path=f"/statistic/?data={StatisticQPData.CASH_AMOUNT.name}")
    response_get_all = login_client.get(path="/statistic/")
    assert len(response_get.data) == 1
    assert response_get.data[0]["amount"] == response_get_all.data[-1]["amount"]


@pytest.mark.parametrize(
    "exp_data",
    [
        pytest.param(
            [
                {
                    "date": "2022-10-03",
                    "loan_create_count": 1,
                    "loan_extend_count": 1,
                    "loan_return_count": 1,
                    "loan_income": 140,
                    "loan_outcome": -100,
                    "loan_profit": 40,
                    "offer_create_count": 0,
                    "offer_sell_count": 1,
                    "offer_income": None,
                    "offer_outcome": 120,
                    "offer_profit": 120,
                    "all_income": 260,
                    "all_outcome": 120,
                    "all_profit": 160,
                },
                {
                    "date": "2022-10-04",
                    "loan_create_count": 2,
                    "loan_extend_count": 1,
                    "loan_return_count": 1,
                    "loan_income": 140,
                    "loan_outcome": -200,
                    "loan_profit": -60,
                    "offer_create_count": 0,
                    "offer_sell_count": 1,
                    "offer_income": None,
                    "offer_outcome": 120,
                    "offer_profit": 120,
                    "all_income": 260,
                    "all_outcome": 120,
                    "all_profit": 60,
                },
            ]
        )
    ],
)
@pytest.mark.django_db
def test_statistic_daily_stats_data(login_client, load_all_fixtures_for_function, exp_data):
    response_get = login_client.get(path=f"/statistic/?data={StatisticQPData.DAILY_STATS.name}")
    assert len(response_get.data) == 2
    assert response_get.data == exp_data


@pytest.mark.parametrize(
    "payload, exp_status",
    [
        pytest.param({"update": f"{StatisticDescription.RESET.name}"}, status.HTTP_201_CREATED),
    ],
)
@pytest.mark.django_db
def test_statistic_reset_profit(login_client, load_all_fixtures_for_module, payload, exp_status):
    response = login_client.post(path="/statistic/", data=payload, format="json")
    response_get = login_client.get(path="/statistic/")
    assert response.status_code == exp_status
    assert len(response_get.data) == 19
    assert response_get.data[-1]["description"] == StatisticDescription.RESET.name
    assert response_get.data[-1]["profit"] == 0
