from rest_framework import mixins, viewsets
from rest_framework.request import Request
from .models import models
from . import serializers


# all
# daily stats
# cash amount
# actual store state: LOAN, OFFER, AFTER_MATURITY
# reset
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
        if "operation" in request.query_params:
            pass
