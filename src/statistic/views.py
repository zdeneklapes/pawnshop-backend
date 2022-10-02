from rest_framework import mixins, viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response
from .models import models
from . import serializers
from common.exceptions import BadQueryParam


class StatisticsGetRequest:
    ALL = "ALL", "Vsechny zaznamy"
    DAILY_STATS = "DAILY_STATS", "Denni statistiky"
    CASH_AMOUNT = "CASH_AMOUT", "Stav pokladny"
    SHOP_STATE = "SHOP_STATE", "Stav obchodu"
    RESET = "RESET", "Reset profit"


class StatisticAllViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = models.Statistic.objects.all()
    serializer_class = serializers.StatisticSerializer

    # permission_classes = [permissions.IsAuthenticated] # TODO: Uncomment

    def list(self, request, *args, **kwargs):
        pass

    def create(self, request: Request, *args, **kwargs):
        # Validate
        if "operation" in request.query_params:
            if request.query_params["operation"] == StatisticsGetRequest.RESET:
                return super(StatisticAllViewSet, self).create(request)

        # Error
        return Response(
            data={"error": f"{StatisticAllViewSet.create.__qualname__} - {BadQueryParam.default_detail}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
