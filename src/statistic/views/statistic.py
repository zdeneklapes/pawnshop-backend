import typing as tp

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import mixins, viewsets, status, permissions, exceptions
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema

import statistic.serializers.all
from statistic.models.models import Statistic
from statistic.serializers import statistic as statistic_serializer
from statistic.models.choices import StatisticQueryParams
from config.settings import AUTH
from statistic.views.permissions import StatisticPermission
from statistic.views.swagger import StatisticQPSwagger


@method_decorator(name="list", decorator=swagger_auto_schema(manual_parameters=[StatisticQPSwagger.data]))
@method_decorator(name="create", decorator=swagger_auto_schema(request_body=StatisticQPSwagger.update))
class StatisticViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Statistic.objects.all()
    serializer_class = statistic_serializer.StatisticSerializer
    permission_classes = (
        [
            StatisticPermission,
            permissions.IsAuthenticated,
        ]
        if AUTH
        else [permissions.AllowAny]
    )

    def parse_data_request(self):
        var_search = "data"

        if (
            var_search not in self.request.query_params
            or self.request.query_params[var_search] not in StatisticQueryParams.names
        ):  # pylint: disable=E1101:
            return None
        else:
            return self.request.query_params[var_search]

    def parse_update_request(self) -> tp.Literal[StatisticQueryParams.names]:
        var_search = "update"

        if var_search not in self.request.data:
            return None  # StatisticQPData.ALL.name

        if self.request.data[var_search] not in StatisticQueryParams.values:  # pylint: disable=E1101:
            return StatisticQueryParams.ALL.name

        return self.request.data[var_search]

    def get_queryset(self):
        data_choice = self.parse_data_request()

        query_sets = {
            StatisticQueryParams.ALL.name: Statistic.objects.all(),
            StatisticQueryParams.CASH_AMOUNT.name: Statistic.objects.get_cash_amount(),
            StatisticQueryParams.DAILY_STATS.name: Statistic.objects.get_daily_stats(),
        }

        try:
            return query_sets[data_choice]
        except KeyError as e:
            raise exceptions.ValidationError({"error": "Bad query"}) from e

    def get_serializer_class(self):
        data_req = self.parse_data_request()
        update_req = self.parse_update_request()

        _map = {
            StatisticQueryParams.ALL.name: statistic.serializers.all.StatisticAllSerializer,
            StatisticQueryParams.CASH_AMOUNT.name: statistic_serializer.StatisticCashAmountSerializer,
            StatisticQueryParams.DAILY_STATS.name: statistic_serializer.StatisticDailyStatsSerializer,
            StatisticQueryParams.RESET.name: statistic_serializer.StatisticSerializer,
        }

        requested_data = {data_req, update_req} & set(_map)  # check if at least one key is in _map
        if requested_data.__len__() != 1:
            raise exceptions.ValidationError({"error": "Expected query parameter: (data) or Data in body (update)"})
        else:
            return _map[requested_data.pop()]

    def list(self, request, *args, **kwargs):
        return super(StatisticViewSet, self).list(request)

    def create(self, request: Request, *args, **kwargs):
        update_req = self.parse_update_request()

        if update_req == StatisticQueryParams.RESET.name:
            return super().create(request)

        # Error
        return Response(
            data={"error": f"{StatisticViewSet.create.__qualname__} - Expected operation type: (RESET, ...)"},
            status=status.HTTP_400_BAD_REQUEST,
        )
