from datetime import datetime

from django.db import models

from authentication.models import CustomerProfile
from product.models import Product
from shop.models import Shop


class Loan(models.Model):
    # Source: https://stackoverflow.com/a/71909815/14471542
    def next_number(self):
        return self._base_manager.filter(date__year=datetime.now().year).count() + 1

    #
    product = models.OneToOneField(to=Product, on_delete=models.CASCADE)
    person = models.OneToOneField(to=CustomerProfile, on_delete=models.CASCADE)
    shop = models.OneToOneField(to=Shop, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    #
    id_for_year = models.PositiveIntegerField(default=next_number, editable=False)
    rate = models.DecimalField(max_digits=3, decimal_places=1)
