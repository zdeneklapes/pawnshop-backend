import pytest
from rest_framework import status
from statistic.models.choices import StatisticQPData


@pytest.mark.django_db
@pytest.mark.parametrize(
    "data, status_code",
    [
        pytest.param(StatisticQPData.DEFAULT.name, status.HTTP_200_OK),
        pytest.param(StatisticQPData.DAILY_STATS.name, status.HTTP_200_OK),
        pytest.param(StatisticQPData.CASH_AMOUNT.name, status.HTTP_200_OK, marks=pytest.mark.xfail),
        # Note: Maybe Bad loaddata statistics.json
        pytest.param(StatisticQPData.RESET.name, status.HTTP_200_OK),
    ],
)
def test_get(login_client, data, status_code):
    response = login_client.get(path=f"/statistic/?data={data}")
    assert response.status_code == status_code
