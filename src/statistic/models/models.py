# pylint: disable=E1101
from django.db import models

from authentication.models.models import User
from product.models.models import Product
from .manager import StatisticManager
from .choices import StatisticDescription


class Statistic(models.Model):
    class Meta:
        permissions = (
            ("view_cash_amount", "Can view cash amount"),
            ("view_daily_stats", "Can view daily stats"),
            ("reset_daily_stats", "Can reset daily stats"),
        )

    objects = StatisticManager()

    # FK
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    #
    datetime = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, choices=StatisticDescription.choices)
    price = models.IntegerField(default=0)
    amount = models.IntegerField()
    profit = models.IntegerField()

    def save(self, *args, **kwargs):
        # Amount
        prev_stat = Statistic.objects.last()
        # Note: if first occurrence (therefore if statement)
        self.amount = self.price + (prev_stat.amount if prev_stat else 0)

        # Profit
        if self.description == StatisticDescription.RESET.name:  # pylint: disable=E1101
            self.profit = 0
        else:
            self.profit = prev_stat.profit + self.price if prev_stat else self.price

        super().save(*args, **kwargs)
