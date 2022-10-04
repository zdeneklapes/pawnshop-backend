import pytest
from rest_framework import status
from statistic.models.choices import StatisticQPData


@pytest.mark.django_db
def test_get_all(client, load_fixtures):
    response = client.get(path="/statistic/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
# @pytest.mark.skip
def test_get_daily_stats(client, load_fixtures):
    response = client.get(path=f"/statistic/?data={StatisticQPData.DAILY_STATS.name}")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.skip
def test_get_shop_stats(client, load_all_fixtures):
    response = client.get(path=f"/statistic/?data={StatisticQPData.SHOP_STATS.name}")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.skip
def test_get_cash_amount(client, load_all_fixtures):
    response = client.get(path=f"/statistic/?data={StatisticQPData.CASH_AMOUNT.name}")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.skip
def test_post_reset(client, load_all_fixtures):
    response = client.post(path=f"/statistic/?data={StatisticQPData.CASH_AMOUNT.name}")
    assert response.status_code == status.HTTP_200_OK
