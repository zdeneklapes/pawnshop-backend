# pylint: disable=E1101
from django.db import models

from .choices import StatisticDescription


class StatisticManager(models.Manager):
    def get_cash_amount(self):
        instance = super().get_queryset().all().last()
        if instance:
            return [{"amount": instance.amount}]
        else:
            return [{"amount": 0}]

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
                offer_income=models.Sum("price", filter=models.Q(description=StatisticDescription.OFFER_SELL.name)),
                offer_outcome=models.Sum("price", filter=models.Q(description=StatisticDescription.OFFER_BUY.name)),
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
                    filter=models.Q(description=StatisticDescription.LOAN_CREATE.name)
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
