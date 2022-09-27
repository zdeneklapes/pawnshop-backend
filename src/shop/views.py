from rest_framework import viewsets

from . import models, serializers


class ShopViewSet(viewsets.ModelViewSet):
    queryset = models.Shop.objects.all()
    serializer_class = serializers.ShopSerializer
