from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import mixins, viewsets, status, permissions
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
        # foo = request.user.groups.filter(name="Member").exists()

        if request.method in permissions.SAFE_METHODS:
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
            permissions.DjangoObjectPermissions,
            permissions.DjangoModelPermissions,
            StatisticPermission,
        ]
        if AUTH
        else [permissions.AllowAny]
    )

    def parse_data_request(self):
        var_search = "data"

        if var_search not in self.request.query_params:
            return StatisticQPData.ALL.name

        if self.request.query_params[var_search] not in StatisticQPData.values:  # pylint: disable=E1101:
            return StatisticQPData.ALL.name

        return self.request.query_params[var_search]

    def parse_update_request(self):
        var_search = "update"

        if var_search not in self.request.data:
            return StatisticQPData.ALL.name

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

        if update_req == StatisticQPData.RESET.name:
            return statistic_serializer.StatisticSerializer  # pylint: disable=E1120

        if data_req == StatisticQPData.ALL.name:
            return statistic_serializer.StatisticAllSerializer  # pylint: disable=E1120

        if data_req == StatisticQPData.CASH_AMOUNT.name:
            return statistic_serializer.StatisticCashAmountSerializer  # pylint: disable=E1120

        if data_req == StatisticQPData.DAILY_STATS.name:
            return statistic_serializer.StatisticDailyStatsSerializer  # pylint: disable=E1120

        return super(StatisticViewSet, self).get_serializer_class()  # default

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
