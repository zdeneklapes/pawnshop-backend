# pylint: disable=E1101
from typing import Optional

from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets, permissions

import product.serializers.product_shop_state
import product.serializers.product_update
from product.serializers import product as product_serializers
from product.models import Product, ProductStatusOrData, ProductShopData
from statistic.serializers.statistic import StatisticSerializer
from statistic.models.choices import StatisticDescription
from common.exceptions import BadQueryParam
from config.settings import AUTH
from .swaggers.product import ProductQPSwagger


@method_decorator(name="list", decorator=swagger_auto_schema(manual_parameters=[ProductQPSwagger.data]))
@method_decorator(name="create", decorator=swagger_auto_schema(manual_parameters=[]))
@method_decorator(name="retrieve", decorator=swagger_auto_schema(manual_parameters=[]))
@method_decorator(name="partial_update", decorator=swagger_auto_schema(request_body=ProductQPSwagger.update))
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = product_serializers.ProductSerializer
    http_method_names = ["get", "post", "patch"]
    permission_classes = [permissions.IsAuthenticated] if AUTH else [permissions.AllowAny]

    def parse_data_request(self):
        var_search = "data"

        if var_search not in self.request.query_params:
            return None

        if self.request.query_params[var_search] in [*ProductStatusOrData.values, *ProductShopData.values]:
            return self.request.query_params[var_search]

        return None

    def parse_update_request(self) -> Optional[str]:
        var_search = "update"

        if var_search not in self.request.data:
            return None

        if self.request.data[var_search] not in StatisticDescription.values:
            return None

        return self.request.data[var_search]

    def get_queryset(self):
        status_or_data = self.parse_data_request()

        if status_or_data == ProductShopData.SHOP_STATS.name:
            return Product.objects.get_shop_state()

        if status_or_data in ProductStatusOrData.values:
            return Product.objects.get_product_by_status(status_or_data)

        return super().get_queryset()

    def get_serializer_class(self):
        update_req = self.parse_update_request()
        status_or_data = self.parse_data_request()

        if status_or_data == ProductShopData.SHOP_STATS.name:
            return product.serializers.product_shop_state.ProductShopStateSerializer

        if update_req in [
            StatisticDescription.LOAN_EXTEND.name,
            StatisticDescription.LOAN_RETURN.name,
            StatisticDescription.LOAN_TO_OFFER.name,
            StatisticDescription.OFFER_SELL.name,
            StatisticDescription.OFFER_BUY.name,
            StatisticDescription.UPDATE_DATA.name,
        ]:
            return product.serializers.product_update.ProductUpdateSerializer

        # TODO: if not GET method raise error
        return super().get_serializer_class()

    # Request Handlers
    def list(self, request, *args, **kwargs):
        return super(ProductViewSet, self).list(request)

    def create(self, request: Request, *args, **kwargs):
        response: Response = super().create(request)  # to internal_repre -> to to_repre

        try:
            StatisticSerializer.save_statistic_product_create(request, response)
        except AssertionError as e:
            return Response(
                {"error": f"{ProductViewSet.create.__qualname__} - {e} - statistics"}, status=response.status_code
            )

        return response

    def partial_update(self, request: Request, *args, **kwargs):
        # Store previous price
        loan = Product.objects.get(pk=request.parser_context["kwargs"]["pk"])
        sell_price_prev = loan.sell_price
        buy_price_prev = loan.buy_price

        response = super().partial_update(request)
        try:
            StatisticSerializer.save_statistic_product_update(request, buy_price_prev, sell_price_prev)
        except BadQueryParam as e:
            return Response(data={"details": f"Statistic - {e}"}, status=BadQueryParam.status_code, exception=True)
        return response
