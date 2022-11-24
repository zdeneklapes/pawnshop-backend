from rest_framework import status
import pytest

from statistic.models.choices import StatisticQueryParams, StatisticDescription


@pytest.mark.parametrize(
    "url, status_code",
    [
        (f"/statistic/?data={StatisticQueryParams.ALL.name}", status.HTTP_200_OK),
        (f"/statistic/?data={StatisticQueryParams.CASH_AMOUNT.name}", status.HTTP_403_FORBIDDEN),
        (f"/statistic/?data={StatisticQueryParams.DAILY_STATS.name}", status.HTTP_403_FORBIDDEN),
    ],
)
@pytest.mark.django_db
def test_attendant_access_data(client_attendant, url, status_code):
    response = client_attendant.get(path=url)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "url, payload, status_code",
    [
        ("/statistic/", {"update": f"{StatisticDescription.RESET.name}"}, status.HTTP_403_FORBIDDEN),
    ],
)
@pytest.mark.django_db
def test_attendant_update(client_attendant, url, payload, status_code):
    response = client_attendant.post(path=url, data=payload, format="json")
    assert response.status_code == status_code
