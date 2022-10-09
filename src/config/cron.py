import sys

from django.db import models

from product.models import Product, ProductStatusOrData
from common import utils


def update_product_status():
    qs_after_maturity = Product.objects.filter(
        models.Q(status=ProductStatusOrData.LOAN.name)  # after_maturity products + set sell_price
        | models.Q(status=ProductStatusOrData.AFTER_MATURITY.name)  # set sell_price
    )

    for loan in qs_after_maturity:
        loan.status = (
            ProductStatusOrData.LOAN.name
            if utils.get_week_delta(loan.date_extend) <= loan.rate_times
            else ProductStatusOrData.AFTER_MATURITY.name
        )

        loan.sell_price = utils.get_sell_price(
            rate=loan.interest_rate_or_quantity, buy_price=loan.buy_price, times=utils.get_week_delta(loan.date_extend)
        )

        loan.save()

    sys.stdout.write("Successfully Updated Loans")


def fun():
    print("hello cron")
    # with open(f"{path.join(BASE_DIR, 'cron_test2.txt')}", "a") as f:
    #     f.write("Hello")
