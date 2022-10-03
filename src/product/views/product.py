from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
import django_filters

from product.serializers import product
from product.models import models
from statistic.serializers import StatisticSerializer
from statistic.models.choices import StatisticOperations
from common.exceptions import BadQueryParam


class ProductQueryParams(django_filters.FilterSet):
    operation = openapi.Parameter(
        name="operation", in_=openapi.IN_QUERY, description="Operation Type", type=openapi.TYPE_STRING
    )
    status = openapi.Parameter(
        name="status", in_=openapi.IN_QUERY, description="Source reference", type=openapi.TYPE_STRING
    )


@method_decorator(name="list", decorator=swagger_auto_schema(manual_parameters=[ProductQueryParams.status]))
@method_decorator(name="create", decorator=swagger_auto_schema(manual_parameters=[]))
@method_decorator(name="retrieve", decorator=swagger_auto_schema(manual_parameters=[]))
@method_decorator(
    name="partial_update", decorator=swagger_auto_schema(manual_parameters=[ProductQueryParams.operation])
)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = product.CreateProductSerializer
    http_method_names = ["get", "post", "patch"]
    # permission_classes = [permissions.IsAuthenticated] # TODO: Uncomment

    # Filters for: "def list()"
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status"]

    def get_serializer_class(self):
        operation = "operation"
        if operation not in self.request.query_params:
            return super().get_serializer_class()
        elif self.request.query_params[operation] == StatisticOperations.LOAN_EXTEND.name:
            return product.LoanExtendSerializer
        elif self.request.query_params[operation] == StatisticOperations.LOAN_RETURN.name:
            return product.LoanReturnSerializer
        elif self.request.query_params[operation] == StatisticOperations.LOAN_TO_OFFER.name:
            return product.LoanToOfferSerializer
        else:
            return super().get_serializer_class()

    # Request Handlers
    def list(self, request, *args, **kwargs):
        return super(ProductViewSet, self).list(request)

    def create(self, request: Request, *args, **kwargs):
        response: Response = super().create(request)  # to internal_repre -> to to_repre
        try:
            StatisticSerializer.save_statistics(
                price=-response.data["buy_price"],
                operation=StatisticOperations.LOAN_CREATE.name,
                user=request.data["user"],  # TODO: change to user: response.user.id
                product=response.data["id"],
            )
        except AssertionError as e:
            return Response(
                data={"error": f"{ProductViewSet.create.__qualname__} - {e} - statistics"}, status=response.status_code
            )
        return response

    def patial_update_save_statistics(self, request: Request, buy_price_prev: int, sell_price_prev: int):
        # Validate
        operation, price = StatisticOperations.validate_operation(request, buy_price_prev, sell_price_prev)

        # Save Statistics
        StatisticSerializer.save_statistics(
            price=price,
            operation=operation,
            user=request.user.id,
            product=request.parser_context["kwargs"]["pk"],
        )

    def partial_update(self, request: Request, *args, **kwargs):
        # Store previous price
        loan = models.Product.objects.get(pk=request.parser_context["kwargs"]["pk"])
        sell_price_prev = loan.sell_price
        buy_price_prev = loan.buy_price

        try:
            response = super().partial_update(request)
            self.patial_update_save_statistics(request, buy_price_prev, sell_price_prev)
        except BadQueryParam as e:
            return Response(
                data={"details": f"Bad query params - {e}"}, status=BadQueryParam.status_code, exception=True
            )
        return response
