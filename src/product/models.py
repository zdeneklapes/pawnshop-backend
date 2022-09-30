from django.db import models


class Product(models.Model):
    #
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
