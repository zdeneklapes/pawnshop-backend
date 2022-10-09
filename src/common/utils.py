import datetime
from datetime import date


def get_week_delta(start_date: datetime.date):
    result = (date.today() - start_date).days // 7 + 1
    return result


def get_sell_price(rate: float, buy_price: int, rate_times: int = 1, base: int = 5):
    price = buy_price + (buy_price * rate * rate_times / 100)
    round_coef = 0 if price % base == 0 else base - (price % base)
    sell_price = price + round_coef
    return sell_price


def get_interests(rate: float, buy_price: int, from_date: datetime.date, rate_times: int = 4):
    """
    Calculate interests of loans and after_maturities
    :param rate:
    :param buy_price:
    :param from_date:
    :param rate_times:
    :return: list of len 4
    """
    delta = get_week_delta(from_date)
    return [
        {
            "from": from_date + datetime.timedelta(weeks=i),
            "to": from_date + datetime.timedelta(weeks=i + 1),
            "price": get_sell_price(rate, buy_price, i + 1),
        }
        for i in range(delta if delta > rate_times else rate_times)
    ][-4:]
