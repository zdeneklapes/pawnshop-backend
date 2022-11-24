import django_filters
from drf_yasg import openapi

from statistic.models import StatisticQueryParams


class StatisticQPSwagger(django_filters.FilterSet):
    data = openapi.Parameter(
        name="data",
        in_=openapi.IN_QUERY,
        description=f"What data you need: "
        f"{StatisticQueryParams.ALL.name}, "  # pylint: disable=E1101
        f"{StatisticQueryParams.DAILY_STATS.name}, "  # pylint: disable=E1101
        f"{StatisticQueryParams.CASH_AMOUNT.name}",  # pylint: disable=E1101
        type=openapi.TYPE_STRING,
    )
    update = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        in_=openapi.IN_BODY,
        properties={
            "update": openapi.Schema(type=openapi.TYPE_STRING, default=f"{StatisticQueryParams.RESET.name}"),
        },
    )
