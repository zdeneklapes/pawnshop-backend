from rest_framework import mixins, viewsets, permissions

from . import models, serializers
from config.settings import AUTH


class ShopViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Shop.objects.all()
    serializer_class = serializers.ShopSerializer
    permission_classes = [permissions.IsAuthenticated] if AUTH else [permissions.AllowAny]
