import pytest
import datetime
from common import utils


@pytest.mark.parametrize(
    "start_date, exp_delta",
    [
        pytest.param(datetime.date.today() - datetime.timedelta(weeks=1), 2),
        pytest.param(datetime.date.today() - datetime.timedelta(weeks=2), 3),
        pytest.param(datetime.date.today() - datetime.timedelta(weeks=3), 4),
    ],
)
def test_get_week_delta(start_date, exp_delta):
    delta = utils.get_week_delta(start_date=start_date)
    assert delta == exp_delta


@pytest.mark.parametrize(
    "rate, buy_price, rate_times, exp_sell_price",
    [
        pytest.param(2.0, 1000, 1, 1020),
        pytest.param(2.1, 1000, 2, 1045),
        pytest.param(2.2, 1000, 3, 1070),
        pytest.param(2.3, 1000, 4, 1095),
    ],
)
def test_get_sell_price(rate: float, buy_price: int, rate_times: int, exp_sell_price: int):
    sell_price = utils.get_sell_price(rate=rate, buy_price=buy_price, rate_times=rate_times)
    assert sell_price == exp_sell_price


@pytest.mark.parametrize(
    "rate, buy_price, rate_times, from_date, exp_dict",
    [
        pytest.param(
            2.0,
            1000,
            4,
            datetime.date.today(),
            [
                {
                    "from": datetime.date.today() + datetime.timedelta(weeks=0),
                    "to": datetime.date.today() + datetime.timedelta(weeks=1),
                    "price": 1020,
                },
                {
                    "from": datetime.date.today() + datetime.timedelta(weeks=1),
                    "to": datetime.date.today() + datetime.timedelta(weeks=2),
                    "price": 1040,
                },
                {
                    "from": datetime.date.today() + datetime.timedelta(weeks=2),
                    "to": datetime.date.today() + datetime.timedelta(weeks=3),
                    "price": 1060,
                },
                {
                    "from": datetime.date.today() + datetime.timedelta(weeks=3),
                    "to": datetime.date.today() + datetime.timedelta(weeks=4),
                    "price": 1080,
                },
            ],
        ),
        pytest.param(
            2.0,
            1000,
            4,
            datetime.date.today() - datetime.timedelta(weeks=6),
            [
                {
                    "from": datetime.date.today() - datetime.timedelta(weeks=3),
                    "to": datetime.date.today() - datetime.timedelta(weeks=2),
                    "price": 1080,
                },
                {
                    "from": datetime.date.today() - datetime.timedelta(weeks=2),
                    "to": datetime.date.today() - datetime.timedelta(weeks=1),
                    "price": 1100,
                },
                {
                    "from": datetime.date.today() - datetime.timedelta(weeks=1),
                    "to": datetime.date.today() - datetime.timedelta(weeks=0),
                    "price": 1120,
                },
                {
                    "from": datetime.date.today() - datetime.timedelta(weeks=0),
                    "to": datetime.date.today() + datetime.timedelta(weeks=1),
                    "price": 1140,
                },
            ],
        ),
    ],
)
def test_get_interests(rate: float, buy_price: int, rate_times: int, from_date: datetime.date, exp_dict):
    interest = utils.get_interests(rate=rate, buy_price=buy_price, from_date=from_date)
    assert interest == exp_dict
