# pylint: disable=E1101
from django.db import models

from authentication.models import User
from product.models.models import Product

from .choices import StatisticDescription


class StatisticManager(models.Manager):
    def get_cash_amount(self):
        instance = super().get_queryset().last()
        return [{"amount": instance.amount}]

    def get_daily_stats(self):
        qs = (
            super()
            .get_queryset()
            .all()
            .annotate(date=models.functions.TruncDay("datetime", models.DateField()))
            .values("date")
            .annotate(
                loan_create_count=models.Count(
                    "price", filter=models.Q(description=StatisticDescription.LOAN_CREATE.name)
                ),
                loan_extend_count=models.Count(
                    "price", filter=models.Q(description=StatisticDescription.LOAN_EXTEND.name)
                ),
                loan_return_count=models.Count(
                    "price", filter=models.Q(description=StatisticDescription.LOAN_RETURN.name)
                ),
                loan_income=models.Sum(
                    "price",
                    filter=models.Q(description=StatisticDescription.LOAN_EXTEND.name)
                    | models.Q(description=StatisticDescription.LOAN_RETURN.name),
                ),
                loan_outcome=models.Sum("price", filter=models.Q(description=StatisticDescription.LOAN_CREATE.name)),
                loan_profit=models.Sum(
                    "price",
                    filter=models.Q(description=StatisticDescription.LOAN_CREATE.name)
                    | models.Q(description=StatisticDescription.LOAN_EXTEND.name)
                    | models.Q(description=StatisticDescription.LOAN_RETURN.name),
                ),
                offer_create_count=models.Count(
                    "price", filter=models.Q(description=StatisticDescription.OFFER_BUY.name)
                ),
                offer_sell_count=models.Count(
                    "price", filter=models.Q(description=StatisticDescription.OFFER_SELL.name)
                ),
                offer_income=models.Sum("price", filter=models.Q(description=StatisticDescription.OFFER_BUY.name)),
                offer_outcome=models.Sum("price", filter=models.Q(description=StatisticDescription.OFFER_SELL.name)),
                offer_profit=models.Sum(
                    "price",
                    filter=models.Q(description=StatisticDescription.OFFER_BUY.name)
                    | models.Q(description=StatisticDescription.OFFER_SELL.name),
                ),
                all_income=models.Sum(
                    "price",
                    filter=models.Q(description=StatisticDescription.LOAN_RETURN.name)
                    | models.Q(description=StatisticDescription.LOAN_EXTEND.name)
                    | models.Q(description=StatisticDescription.OFFER_SELL.name),
                ),
                all_outcome=models.Sum(
                    "price",
                    filter=models.Q(description=StatisticDescription.OFFER_SELL.name)
                    | models.Q(description=StatisticDescription.OFFER_BUY.name),
                ),
                all_profit=models.Sum(
                    "price",
                    filter=models.Q(description=StatisticDescription.LOAN_CREATE.name)
                    | models.Q(description=StatisticDescription.LOAN_EXTEND.name)
                    | models.Q(description=StatisticDescription.LOAN_RETURN.name)
                    | models.Q(description=StatisticDescription.OFFER_BUY.name)
                    | models.Q(description=StatisticDescription.OFFER_SELL.name),
                ),
            )
            .values(
                "date",
                "loan_create_count",
                "loan_extend_count",
                "loan_return_count",
                "loan_income",
                "loan_outcome",
                "loan_profit",
                "offer_create_count",
                "offer_sell_count",
                "offer_income",
                "offer_outcome",
                "offer_profit",
                "all_income",
                "all_outcome",
                "all_profit",
            )
        )
        return qs


class Statistic(models.Model):
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
        amount = prev_stat.amount if prev_stat else 0  # if first occurrence
        self.amount = self.price + amount

        # Profit
        if self.description == StatisticDescription.RESET.name:  # pylint: disable=E1101
            self.profit = 0
        else:
            self.profit = prev_stat.profit + self.price if prev_stat else self.price

        super().save(*args, **kwargs)
