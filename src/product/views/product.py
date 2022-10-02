from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.request import Request
from rest_framework import response, viewsets
from django_filters.rest_framework import DjangoFilterBackend
import django_filters

from product.serializers import product
from product.models import models
from statistic.serializers import StatisticSerializer
from statistic.models.choices import StatisticOperation


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

    # Filters for: "def list()"
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status"]

    def get_serializer_class(self):
        operation = "operation"
        if operation not in self.request.query_params:
            return super().get_serializer_class()
        elif self.request.query_params[operation] == StatisticOperation.LOAN_EXTEND.name:
            return product.LoanExtendSerializer
        elif self.request.query_params[operation] == StatisticOperation.LOAN_RETURN.name:
            return product.LoanReturnSerializer
        elif self.request.query_params[operation] == StatisticOperation.LOAN_TO_OFFER.name:
            return product.LoanToOfferSerializer
        else:
            return super().get_serializer_class()

    # Request Handlers
    def list(self, request, *args, **kwargs):
        return super(ProductViewSet, self).list(request)

    def create(self, request: Request, *args, **kwargs):
        try:
            response_: response.Response = super().create(request)  # to internal_repre -> to to_repre
            StatisticSerializer.save_statistics(
                price=response_.data["buy_price"],
                operation=StatisticOperation.LOAN_CREATE.name,
                user=response_.data["user"],
                product=response_.data["id"],
            )
        except AssertionError as e:
            return response.Response(
                data={"error": f"{ProductViewSet.create.__qualname__}: {e}"}, status=response_.status_code
            )
        return response_

    def partial_update(self, request: Request, *args, **kwargs):
        # TODO: Statistics save, be carefully in writing description
        if "operation" not in request.query_params:
            pass
        return super().partial_update(request)
