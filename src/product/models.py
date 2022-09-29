from django.db import models

from authentication.models import CustomerProfile
from shop.models import Shop


class Product(models.Model):
    #
    person = models.OneToOneField(to=CustomerProfile, on_delete=models.CASCADE)
    shop = models.OneToOneField(to=Shop, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    #
    description = models.TextField()
    buy_price = models.PositiveIntegerField()
    sell_price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)

    #
    date_create = models.DateTimeField()
    date_extended_deadline = models.DateTimeField(null=True)
    date_end = models.DateTimeField(null=True)  # return/sell
