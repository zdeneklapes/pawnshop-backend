from rest_framework import viewsets, mixins, permissions

from . import models, serializers


class CashDeskViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = models.CashDesk.objects.all()
    serializer_class = serializers.CashDeskSerializer
    permission_classes = [permissions.IsAuthenticated]
