from datetime import datetime, timedelta, date

from django.db import models

from authentication.models import CustomerProfile, User
from product.models import Product
from shop.models import Shop


def next_number():
    """Source: https://stackoverflow.com/a/71909815/14471542"""
    return Loan.objects.filter(date_created__year=datetime.now().year).count() + 1


class LoanBeforeMaturityManager(models.Manager):
    def before_maturity(self):
        startdate = date.today() - timedelta(weeks=4)

        qs_products = Product.objects.filter(date_create__gte=startdate)
        qs_loans = (
            super(LoanBeforeMaturityManager, self)
            .get_queryset()
            .filter(product__in=qs_products.values("id"), is_active=True)
        )
        for loan in qs_loans:
            Product.objects.get(id=loan.product.id).update_sell_price_based_on_week(
                rate=loan.rate
            )

        return (
            super(LoanBeforeMaturityManager, self)
            .get_queryset()
            .filter(product__in=qs_products.values("id"), is_active=True)
        )


class LoanAfterMaturityManager(models.Manager):
    def after_maturity(self):
        startdate = date.today() - timedelta(weeks=4)
        qs_products = Product.objects.filter(date_create__lt=startdate)
        return (
            super(LoanAfterMaturityManager, self)
            .get_queryset()
            .filter(product__in=qs_products.values("id"), is_active=True)
        )


class Loan(models.Model):
    # Managers
    objects = models.Manager()
    before_maturity = LoanBeforeMaturityManager()
    after_maturity = LoanAfterMaturityManager()

    #
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(to=CustomerProfile, on_delete=models.CASCADE)
    shop = models.ForeignKey(to=Shop, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    #
    id_for_year = models.PositiveIntegerField(default=next_number, editable=False)
    rate = models.DecimalField(max_digits=4, decimal_places=1)
