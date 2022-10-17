# pylint: disable=E1101
from drf_yasg import openapi

import django_filters

from product.models import ProductShopData, ProductStatusOrData
from statistic.models.choices import StatisticDescription


class ProductQPSwagger(django_filters.FilterSet):
    data = openapi.Parameter(
        name="data",
        in_=openapi.IN_QUERY,
        description=f"Operation Type: "
        f"{ProductShopData.SHOP_STATS.name}, "
        f"{ProductStatusOrData.LOAN.name}, "
        f"{ProductStatusOrData.OFFER.name}, "
        f"{ProductStatusOrData.AFTER_MATURITY.name}",
        type=openapi.TYPE_STRING,
    )
    update = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        in_=openapi.IN_BODY,
        properties={
            "update": openapi.Schema(
                type=openapi.TYPE_STRING,
                default=f"{StatisticDescription.LOAN_RETURN.name} | "
                f"{StatisticDescription.LOAN_EXTEND.name} | "
                f"{StatisticDescription.LOAN_TO_OFFER.name} | "
                f"{StatisticDescription.OFFER_SELL.name} | "
                f"{StatisticDescription.OFFER_BUY.name} | "
                f"{StatisticDescription.UPDATE_DATA.name}",
            ),
            "product_name": openapi.Schema(type=openapi.TYPE_STRING),
            "sell_price": openapi.Schema(type=openapi.TYPE_STRING),
            "date_create": openapi.Schema(type=openapi.TYPE_STRING),
            "date_extend": openapi.Schema(type=openapi.TYPE_STRING),
            "inventory_id": openapi.Schema(type=openapi.TYPE_STRING),
        },
    )
