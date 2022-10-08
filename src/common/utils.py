from datetime import date


def get_week_delta(start_date):
    result = (date.today() - start_date.date()).days // 7 + 1
    return result


def get_sell_price(rate: float, buy_price: int, times: int = 1, base: int = 5):
    price = buy_price + (buy_price * rate * times / 100)
    round_coef = base if price % base != 0 else base - (price % base)
    return base * round(price / base) + round_coef
