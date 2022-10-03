from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import mixins, viewsets, status
from django.utils.decorators import method_decorator
from django.db import models
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import django_filters

from .models.models import Statistic
from . import serializers
from common.exceptions import BadQueryParam


class StatisticsQueryParamsChoices(models.TextChoices):
    ALL = "ALL", "Vsechny zaznamy"
    DAILY_STATS = "DAILY_STATS", "Denni statistiky"
    CASH_AMOUNT = "CASH_AMOUT", "Stav pokladny"
    SHOP_STATE = "SHOP_STATE", "Stav obchodu"
    RESET = "RESET", "Reset profit"


class StatisticQueryParamsSwagger(django_filters.FilterSet):
    data = openapi.Parameter(
        name="data",
        in_=openapi.IN_QUERY,
        description=f"What data you need: "
        f"{StatisticsQueryParamsChoices.ALL.name}, "  # pylint: disable=E1101
        f"{StatisticsQueryParamsChoices.DAILY_STATS.name}, "  # pylint: disable=E1101
        f"{StatisticsQueryParamsChoices.CASH_AMOUNT.name}",  # pylint: disable=E1101
        type=openapi.TYPE_STRING,
    )
    operation = openapi.Parameter(
        name="operation",
        in_=openapi.IN_QUERY,
        description=f"What should be done: {StatisticsQueryParamsChoices.RESET.name}",  # pylint: disable=E1101
        type=openapi.TYPE_STRING,
    )


@method_decorator(name="list", decorator=swagger_auto_schema(manual_parameters=[StatisticQueryParamsSwagger.data]))
@method_decorator(
    name="create", decorator=swagger_auto_schema(manual_parameters=[StatisticQueryParamsSwagger.operation])
)
class StatisticViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Statistic.objects.all()
    serializer_class = serializers.StatisticSerializer

    # permission_classes = [permissions.IsAuthenticated] # TODO: Uncomment

    def get_queryset(self):
        if "data" not in self.request.query_params:
            return super(StatisticViewSet, self).get_queryset()

        data = self.request.query_params["data"]
        if data == StatisticsQueryParamsChoices.ALL.name:  # pylint: disable=E1101
            return super(StatisticViewSet, self).get_queryset()
        elif data == StatisticsQueryParamsChoices.CASH_AMOUNT.name:  # pylint: disable=E1101
            return Statistic.objects.get_cash_amount()  # pylint: disable=E1120
        else:  # TODO: Create some Response that tell user the request was with bad params
            return super(StatisticViewSet, self).get_queryset()

    def get_statistic_queryparams_choice(self, request) -> str:
        if "data" in self.request.query_params:
            return self.request.query_params["data"]

    def list(self, request, *args, **kwargs):
        if (
            self.get_statistic_queryparams_choice(request)
            == StatisticsQueryParamsChoices.DAILY_STATS.name  # pylint: disable=E1101
        ):
            pass
        else:
            return super(StatisticViewSet, self).list(request)

    def create(self, request: Request, *args, **kwargs):
        # Validate
        if "operation" in request.query_params:
            if request.query_params["operation"] == StatisticsQueryParamsChoices.RESET:
                return super(StatisticViewSet, self).create(request)

        # Error
        return Response(
            data={"error": f"{StatisticViewSet.create.__qualname__} - {BadQueryParam.default_detail}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
