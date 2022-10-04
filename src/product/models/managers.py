# pylint: disable=E1101
from typing import Literal

from django.db import models

from .choices import ProductStatus


class ProductManager(models.Manager):
    def get_product_by_status(
        self, status: Literal[ProductStatus.LOAN.name, ProductStatus.OFFER.name, ProductStatus.AFTER_MATURITY.name]
    ):
        qs = super(ProductManager, self).get_queryset().filter(status=status)
        return qs

    def get_shop_state(self):
        qs = super().get_queryset().all().values("status").annotate(count=models.Count("status"))
        return qs
