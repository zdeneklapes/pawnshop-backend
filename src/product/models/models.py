import datetime
from django.db import models

from authentication.models import User
from customer.models import CustomerProfile
from .choices import ProductStatusOrData, RateFrequency
from .managers import ProductManager


class Product(models.Model):
    status = models.CharField(max_length=50, choices=ProductStatusOrData.choices)

    # Managers
    objects = ProductManager()

    # FK
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    customer = models.ForeignKey(to=CustomerProfile, on_delete=models.CASCADE)

    # Rate
    rate_frequency = models.CharField(max_length=50, choices=RateFrequency.choices, default="WEEK")
    rate_times = models.PositiveIntegerField(default=4)
    interest_rate_or_quantity = models.DecimalField(max_digits=4, decimal_places=1, null=True)

    # Product
    product_name = models.TextField()
    buy_price = models.PositiveIntegerField()
    sell_price = models.PositiveIntegerField(null=True)  # Cron
    # quantity = models.PositiveIntegerField(default=1)
    inventory_id = models.PositiveIntegerField()

    # Dates
    date_create = models.DateTimeField(null=True)
    date_extend = models.DateTimeField(null=True)
    date_end = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if not self.date_create:
            self.date_create = datetime.datetime.now()

        if not self.date_extend:
            self.date_extend = datetime.datetime.now()

        if not self.date_end:
            self.date_end = (self.date_extend.date() + datetime.timedelta(weeks=self.rate_times)).__str__()

        return super().save(*args, **kwargs)
