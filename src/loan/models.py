from datetime import datetime

from django.db import models

from authentication.models import CustomerProfile, User
from product.models import Product
from shop.models import Shop


def next_number():
    """Source: https://stackoverflow.com/a/71909815/14471542"""
    return Loan.objects.filter(date_created__year=datetime.now().year).count() + 1


class Loan(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)

    #
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(to=CustomerProfile, on_delete=models.CASCADE)
    shop = models.ForeignKey(to=Shop, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    #
    id_for_year = models.PositiveIntegerField(default=next_number, editable=False)
    rate = models.DecimalField(max_digits=4, decimal_places=1)
