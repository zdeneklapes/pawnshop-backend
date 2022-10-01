def get_sell_price(rate: float, buy_price: int, base: int = 5):
    price = buy_price + buy_price * rate / 100
    return base * round(price / base) + base
