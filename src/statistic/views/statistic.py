import typing as tp

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import mixins, viewsets, status, permissions, exceptions
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema

from statistic.models.models import Statistic
from statistic.serializers import statistic as statistic_serializer
from statistic.models.choices import StatisticQPData
from config.settings import AUTH
from statistic.views.swagger import StatisticQPSwagger


# TODO: where to handle user permissions?
# TODO: where to set permissions for each user?
# TODO: groups vs. permissions?


class StatisticPermission(permissions.BasePermission):
    def has_permission(self, request: Request, view: "StatisticViewSet") -> bool:
        # foo = request.user.groups.filter(name=).exists()
        if request.method == "GET" and request.query_params.get("data") == StatisticQPData.ALL:
            return request.user.has_perm("statistic.view_statistic")
        return request.user.has_perm("statistic.reset_daily_stats")


@method_decorator(name="list", decorator=swagger_auto_schema(manual_parameters=[StatisticQPSwagger.data]))
@method_decorator(name="create", decorator=swagger_auto_schema(request_body=StatisticQPSwagger.update))
class StatisticViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Statistic.objects.all()
    serializer_class = statistic_serializer.StatisticSerializer
    permission_classes = (
        [
            permissions.IsAuthenticated,
            # StatisticPermission
        ]
        if AUTH
        else [permissions.AllowAny]
    )

    def parse_data_request(self):
        var_search = "data"

        if (
            var_search not in self.request.query_params
            or self.request.query_params[var_search] not in StatisticQPData.names
        ):  # pylint: disable=E1101:
            return None
        else:
            return self.request.query_params[var_search]

    def parse_update_request(self) -> tp.Literal[StatisticQPData.names]:
        var_search = "update"

        if var_search not in self.request.data:
            return None  # StatisticQPData.ALL.name

        if self.request.data[var_search] not in StatisticQPData.values:  # pylint: disable=E1101:
            return StatisticQPData.ALL.name

        return self.request.data[var_search]

    def get_queryset(self):
        data_choice = self.parse_data_request()

        if data_choice == StatisticQPData.CASH_AMOUNT.name:
            # TODO: Return object and not array of one object
            return Statistic.objects.get_cash_amount()  # pylint: disable=E1120

        if data_choice == StatisticQPData.DAILY_STATS.name:
            return Statistic.objects.get_daily_stats()

        return super(StatisticViewSet, self).get_queryset()  # default

    def get_serializer_class(self):
        data_req = self.parse_data_request()
        update_req = self.parse_update_request()

        _map = {
            StatisticQPData.ALL.name: statistic_serializer.StatisticAllSerializer,
            StatisticQPData.CASH_AMOUNT.name: statistic_serializer.StatisticCashAmountSerializer,
            StatisticQPData.DAILY_STATS.name: statistic_serializer.StatisticDailyStatsSerializer,
            StatisticQPData.RESET.name: statistic_serializer.StatisticSerializer,
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

        if update_req == StatisticQPData.RESET.name:
            return super().create(request)

        # Error
        return Response(
            data={"error": f"{StatisticViewSet.create.__qualname__} - Expected operation type: (RESET, ...)"},
            status=status.HTTP_400_BAD_REQUEST,
        )
