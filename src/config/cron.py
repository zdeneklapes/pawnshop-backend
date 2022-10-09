import sys
import os
from os import path

from django.db import models

from config.settings import BASE_DIR
from product.models import Product, ProductStatusOrData
from common import utils


def update_product_status():
    print("hello cron")
    with open(f"{path.join(BASE_DIR, 'cron_test1.txt')}", "a") as f:
        f.write("Hello1")
        f.write(os.environ.get("DJANGO_SETTINGS_MODULE"))

    qs_after_maturity = Product.objects.filter(
        models.Q(status=ProductStatusOrData.LOAN.name)  # after_maturity products + set sell_price
        | models.Q(status=ProductStatusOrData.AFTER_MATURITY.name)  # set sell_price
    )

    with open(f"{path.join(BASE_DIR, 'cron_test1.txt')}", "a") as f:
        f.write("Hello2\n")
        f.write(f"|{qs_after_maturity}|")
        f.write(f"|{qs_after_maturity}|")

    for loan in qs_after_maturity:
        with open(f"{path.join(BASE_DIR, 'cron_test1.txt')}", "a") as f:
            f.write("Hello3")

        loan.status = (
            ProductStatusOrData.LOAN.name
            if utils.get_week_delta(loan.date_extend) <= loan.rate_times
            else ProductStatusOrData.AFTER_MATURITY.name
        )

        with open(f"{path.join(BASE_DIR, 'cron_test1.txt')}", "a") as f:
            f.write("Hello4")

        loan.sell_price = utils.get_sell_price(
            rate=loan.interest_rate_or_quantity, buy_price=loan.buy_price, times=utils.get_week_delta(loan.date_extend)
        )

        with open(f"{path.join(BASE_DIR, 'cron_test1.txt')}", "a") as f:
            f.write("Hello5")

        loan.save()

        with open(f"{path.join(BASE_DIR, 'cron_test1.txt')}", "a") as f:
            f.write("Hello6")

    sys.stdout.write("Successfully Updated Loans")

    #
    print("hello cron")
    with open(f"{path.join(BASE_DIR, 'cron_test1.txt')}", "a") as f:
        f.write("Hello7")


def fun():
    print("hello cron")
    with open(f"{path.join(BASE_DIR, 'cron_test2.txt')}", "a") as f:
        f.write("Hello")
