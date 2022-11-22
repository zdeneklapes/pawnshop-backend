import django_filters
from drf_yasg import openapi

from statistic.models import StatisticQPData


class StatisticQPSwagger(django_filters.FilterSet):
    data = openapi.Parameter(
        name="data",
        in_=openapi.IN_QUERY,
        description=f"What data you need: "
        f"{StatisticQPData.ALL.name}, "  # pylint: disable=E1101
        f"{StatisticQPData.DAILY_STATS.name}, "  # pylint: disable=E1101
        f"{StatisticQPData.CASH_AMOUNT.name}",  # pylint: disable=E1101
        type=openapi.TYPE_STRING,
    )
    update = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        in_=openapi.IN_BODY,
        properties={
            "update": openapi.Schema(type=openapi.TYPE_STRING, default=f"{StatisticQPData.RESET.name}"),
        },
    )
