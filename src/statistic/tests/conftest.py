import pytest
from statistic.models.choices import StatisticQueryParams


def pytest_configure():
    statistic_urls = {
        key: f"/statistic/?data={key}" for key in StatisticQueryParams.names if key != StatisticQueryParams.RESET.name
    }
    statistic_urls[StatisticQueryParams.RESET.name] = "/statistic/"
    pytest.statistic_urls = statistic_urls
