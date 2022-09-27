from rest_framework import viewsets

from . import models, serializers


class ShopViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """

    queryset = models.Shop.objects.all()
    serializer_class = serializers.ShopSerializer
