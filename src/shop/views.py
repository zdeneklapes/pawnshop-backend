from rest_framework import mixins, viewsets

from . import models, serializers


class ShopViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Shop.objects.all()
    serializer_class = serializers.ShopSerializer
    # permission_classes = [permissions.IsAuthenticated] # TODO: Uncomment
