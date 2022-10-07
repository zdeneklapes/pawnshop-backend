# pylint: disable=E1101
from typing import Literal

from django.db import models

from .choices import ProductStatusOrData


class ProductManager(models.Manager):
    def get_product_by_status(
        self,
        status: Literal[
            ProductStatusOrData.LOAN.name, ProductStatusOrData.OFFER.name, ProductStatusOrData.AFTER_MATURITY.name
        ],
    ):
        qs = super(ProductManager, self).get_queryset().filter(status=status)
        return qs

    def get_shop_state(self):
        qs = (
            super()
            .get_queryset()
            .filter(
                models.Q(status=ProductStatusOrData.LOAN.name)
                | models.Q(status=ProductStatusOrData.OFFER.name)
                | models.Q(status=ProductStatusOrData.AFTER_MATURITY.name)
            )
            .values("status")
            .order_by("status")
            .annotate(count=models.Count("status"))
            .annotate(buy=models.Sum("buy_price"))
            .annotate(sell=models.Sum("sell_price"))
        )
        return qs
