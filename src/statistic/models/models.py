from django.db import models

from authentication.models import User
from product.models.models import Product

from .choices import StatisticOperation


class Statistic(models.Model):
    # FK
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    #
    description = models.CharField(max_length=255, choices=StatisticOperation.choices)
    price = models.IntegerField()
    amount = models.IntegerField()

    def save(self, *args, **kwargs):
        prev_amount = Statistic.objects.last()
        amount = prev_amount.amount if prev_amount else 0  # if first occurrence
        self.amount = self.price + amount
        super().save(*args, **kwargs)
