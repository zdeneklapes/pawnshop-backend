import pytest
from rest_framework import status
from statistic.models.choices import StatisticQueryParams


@pytest.mark.django_db
@pytest.mark.parametrize(
    "data, status_code",
    [
        pytest.param(StatisticQueryParams.ALL.name, status.HTTP_200_OK),
        pytest.param(StatisticQueryParams.DAILY_STATS.name, status.HTTP_200_OK),
        pytest.param(StatisticQueryParams.CASH_AMOUNT.name, status.HTTP_200_OK),
        pytest.param(StatisticQueryParams.RESET.name, status.HTTP_403_FORBIDDEN),  # bad query param
    ],
)
def test_get(client_admin, data, status_code):
    response = client_admin.get(path=f"/statistic/?data={data}")
    assert response.status_code == status_code


@pytest.mark.skip(reason="Not implemented")
def test_get_all_values(client_admin):
    # TODO: test id, datetime, description, price, product, username, product_name, amount, profit
    # all fields must be in response.data
    pass
