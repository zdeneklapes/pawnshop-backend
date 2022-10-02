from rest_framework import mixins, viewsets
from .models import models
from . import serializers


class StatisticAllViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Statistic.objects.all()
    serializer_class = serializers.StatisticSerializer
    # permission_classes = [permissions.IsAuthenticated]


class StatisticDailyViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Statistic.objects.all()
    serializer_class = serializers.StatisticSerializer
    # permission_classes = [permissions.IsAuthenticated]


class StatisticResetViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Statistic.objects.all()
    serializer_class = serializers.StatisticSerializer
    # permission_classes = [permissions.IsAuthenticated]
