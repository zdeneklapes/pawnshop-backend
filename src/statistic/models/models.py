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
            ("reset_profit", "Can reset profit"),
        )

    objects = StatisticManager()

    # FK
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    #
    datetime = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, choices=StatisticDescription.choices)
    price = models.IntegerField(default=None, null=True)
    amount = models.IntegerField()
    profit = models.IntegerField()

    def save(self, *args, **kwargs):
        # Amount
        statistic_prev = Statistic.objects.last()
        statistic_amount_prev = statistic_prev.amount if statistic_prev else 0
        statistic_profit_prev = statistic_prev.profit if statistic_prev else 0
        # Note: if first occurrence (therefore if statement)

        # Amount
        if self.price:
            self.amount = statistic_amount_prev + self.price
        else:
            self.amount = statistic_amount_prev

        # Profit
        if self.description == StatisticDescription.RESET.name:  # pylint: disable=E1101
            self.profit = 0
        else:
            if self.price:
                self.profit = statistic_profit_prev + self.price
            else:
                self.profit = statistic_profit_prev

        #
        super().save(*args, **kwargs)
