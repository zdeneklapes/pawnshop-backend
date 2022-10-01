from django.db import models
from .choices import ProductStatus


class ProductManager(models.Manager):
    def get_offers(self):
        qs = super(ProductManager, self).get_queryset().filter(status=ProductStatus.OFFER.name)  # pylint: disable=E1101
        return qs

    def get_loans(self):
        qs = super(ProductManager, self).get_queryset().filter(status=ProductStatus.LOAN.name)  # pylint: disable=E1101
        return qs

    def get_after_maturity(self):
        qs = (
            super(ProductManager, self)
            .get_queryset()
            .filter(status=ProductStatus.AFTER_MATURITY.name)  # pylint: disable=E1101
        )
        return qs
