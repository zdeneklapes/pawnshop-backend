import datetime
from datetime import date


def get_week_delta(start_date: datetime):
    result = (date.today() - start_date.date()).days // 7 + 1
    return result


def get_sell_price(rate: float, buy_price: int, times: int = 1, base: int = 5):
    price = buy_price + (buy_price * rate * times / 100)
    round_coef = base if price % base != 0 else base - (price % base)
    return base * round(price / base) + round_coef


def get_interests(rate: float, buy_price: int, rate_times: int, from_date: datetime):
    delta = get_week_delta(from_date)
    return [
        {
            "from": from_date + datetime.timedelta(weeks=i),
            "to": from_date + datetime.timedelta(weeks=i + 1),
            "price": get_sell_price(rate, buy_price, i + 1),
        }
        for i in range(delta if delta > 4 else rate_times)
    ][-4:]
