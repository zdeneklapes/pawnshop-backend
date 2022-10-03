from django.db import models

from authentication.models import User
from product.models.models import Product

from .choices import StatisticOperations


class StatisticManager(models.Manager):
    def get_cash_amount(self):
        instance = super().get_queryset().last()  # pylint: disable=E1101
        return [{"amount": instance.amount}]

    def get_daily_stats(self):
        return [
            {
                "date": "2022-10-10",
                "LOAN_CREATE": 1,
                "LOAN_EXTENDS": 1,
                "LOAN_RETURN": 1,
                "loan_income": 100,
                "loan_outcome": 100,
                "loan_profit": 100,
                "OFFER_CREATE": 1,
                "OFFER_SELL": 1,
                "offer_income": 100,
                "offer_outcome": 100,
                "offer_profit": 100,
                "all_income": 1,
                "all_outcome": 1,
                "all_profit": 1,
            }
        ]

    def get_shop_state(self):
        pass


class Statistic(models.Model):
    objects = StatisticManager()

    # FK
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    #
    datetime = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, choices=StatisticOperations.choices)
    price = models.IntegerField(default=0)
    amount = models.IntegerField()
    profit = models.IntegerField()

    def save(self, *args, **kwargs):
        # Amount
        prev_stat = Statistic.objects.last()
        amount = prev_stat.amount if prev_stat else 0  # if first occurrence
        self.amount = self.price + amount

        # Profit
        if self.description == StatisticOperations.RESET.name:  # pylint: disable=E1101
            self.profit = 0
        else:
            self.profit = prev_stat.profit + self.price if prev_stat else self.price

        super().save(*args, **kwargs)
