from rest_framework import permissions, viewsets
from .models import models
from . import serializers


class StatisticAllViewSet(viewsets.ModelViewSet):
    queryset = models.Statistic.objects.all()
    serializer_class = serializers.StatisticSerializer
    permission_classes = [permissions.IsAuthenticated]
