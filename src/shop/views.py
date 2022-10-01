from rest_framework import viewsets, mixins, permissions

from . import models, serializers


class ShopViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Shop.objects.all()
    serializer_class = serializers.ShopSerializer
    permission_classes = [permissions.IsAuthenticated]
