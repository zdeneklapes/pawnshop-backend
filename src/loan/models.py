from datetime import datetime, timedelta, date

from django.db import models

from authentication.models import CustomerProfile, User
from product.models import Product
from shop.models import Shop


def next_number():
    """Source: https://stackoverflow.com/a/71909815/14471542"""
    return Loan.objects.filter(date_created__year=datetime.now().year).count() + 1


class LoanManager(models.Manager):
    @property
    def start_date(self):
        startdate = date.today() - timedelta(weeks=4)
        return startdate

    def before_maturity(self):
        qs_products = Product.objects.filter(
            date_create__gte=self.start_date
        ) | Product.objects.filter(date_extended_deadline__gte=self.start_date)
        # qs_loans = (
        #     super(LoanManager, self)
        #     .get_queryset()
        #     .filter(product__in=qs_products.values("id"), is_active=True)
        # )
        # for loan in qs_loans:
        #     Product.objects.get(id=loan.product.id).update_sell_price_based_on_week(
        #         rate=loan.rate
        #     )

        return (
            super(LoanManager, self)
            .get_queryset()
            .filter(product__in=qs_products.values("id"), is_active=True)
        )

    def after_maturity(self):
        qs_products = Product.objects.filter(
            date_create__lt=self.start_date
        ) | Product.objects.filter(date_extended_deadline__lt=self.start_date)
        # qs_loans = (
        #     super(LoanManager, self)
        #     .get_queryset()
        #     .filter(product__in=qs_products.values("id"), is_active=True)
        # )
        # for loan in qs_loans:
        #     Product.objects.get(id=loan.product.id).update_sell_price_based_on_week(
        #         rate=loan.rate
        #     )
        return (
            super(LoanManager, self)
            .get_queryset()
            .filter(product__in=qs_products.values("id"), is_active=True)
        )


class Loan(models.Model):
    # Managers
    objects = LoanManager()

    #
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(to=CustomerProfile, on_delete=models.CASCADE)
    shop = models.ForeignKey(to=Shop, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    #
    id_for_year = models.PositiveIntegerField(default=next_number, editable=False)
    rate = models.DecimalField(max_digits=4, decimal_places=1)

    date_created = models.DateTimeField(auto_now_add=True, null=True)
