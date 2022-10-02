from django.utils import timezone
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import requests
from rest_framework import mixins, response, status, viewsets
from django_filters.rest_framework import DjangoFilterBackend
import django_filters

from product.serializers import product
from product.models import models, choices
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

    def serializer_operation(self):
        operation = "operation"
        if operation not in self.request.query_params:
            return None
        elif self.request.query_params[operation] == StatisticOperation.LOAN_EXTEND.name:
            return product.ExtendLoanSerializer
        elif self.request.query_params[operation] == StatisticOperation.MOVE_LOAN_TO_BAZAR.name:
            return None
        elif self.request.query_params[operation] == StatisticOperation.LOAN_RETURN.name:
            return None
        else:
            return None

    def get_serializer_class(self):
        serializer = self.serializer_operation()
        return serializer if serializer else super(ProductViewSet, self).get_serializer_class()

    def list(self, request, *args, **kwargs):
        return super(ProductViewSet, self).list(request)

    def create(self, request: requests.Request, *args, **kwargs):
        response_ = super().create(request)  # to internal_repre -> to to_repre
        try:
            StatisticSerializer.save_statistics(
                price=response_.data["buy_price"],
                operation=StatisticOperation.LOAN_CREATE.name,
                user=response_.data["user"],
                product=response_.data["id"],
            )
        except AssertionError as e:
            return response.Response(
                data={"error": f"{ProductViewSet.create.__qualname__}: {e}"}, status=status.HTTP_400_BAD_REQUEST
            )
        return response_

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request)


class ExtendLoanViewSet(
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Product.objects.all()
    serializer_class = product.ExtendLoanSerializer
    http_method_names = ["patch"]

    # permission_classes = [permissions.IsAuthenticated] # TODO: Uncomment

    # def create_data(self, loan: models.Product):
    #     return {
    #         "status": models.ProductStatus.LOAN.name,
    #         "sell_price": utils.get_sell_price(rate=loan.rate, buy_price=loan.buy_price),
    #         "date_extend": timezone.now(),
    #     }

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request)


class ReturnLoanViewSet(
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Product.objects.all()
    serializer_class = product.CreateProductSerializer
    http_method_names = ["patch"]

    # permission_classes = [permissions.IsAuthenticated]

    def create_data(self):
        return {"status": choices.ProductStatus.INACTIVE_LOAN.name, "date_end": timezone.now()}

    def partial_update(self, request, *args, **kwargs):
        # TODO: Return only LOAN and AFTER_MATURITY
        request.data.update(self.create_data())
        return super().partial_update(request)


class LoanToBazarViewSet(
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Product.objects.all()
    serializer_class = product.CreateProductSerializer
    http_method_names = ["patch"]

    # permission_classes = [permissions.IsAuthenticated]

    def create_data(self, request: requests.Request):
        return {"status": choices.ProductStatus.OFFER.name, "sell_price": request.data["product_sell"]}

    def partial_update(self, request, *args, **kwargs):
        # TODO: Move only AFTER_MATURITY
        request.data.update(self.create_data(request))
        return super().partial_update(request)
