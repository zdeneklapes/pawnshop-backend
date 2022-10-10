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
def test_after_aturity_extend(login_client):
    assert False


@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
@pytest.mark.django_db
@pytest.mark.xfail
def test_offer_create(login_client):
    assert False


@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
@pytest.mark.django_db
@pytest.mark.xfail
def test_offer_buy(login_client):
    assert False


@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
@pytest.mark.django_db
@pytest.mark.xfail
def test_offer_sell(login_client):
    assert False


@pytest.mark.parametrize(
    "",
    [
        pytest.param(),
    ],
)
@pytest.mark.django_db
@pytest.mark.xfail
def test_statistic_default_data(login_client):
    assert False


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
