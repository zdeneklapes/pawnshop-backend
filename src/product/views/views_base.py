from rest_framework import mixins, permissions, response, viewsets

from product import models, serializers
from product.models import Product


class LoanViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Product.objects.all()
    serializer_class = serializers.LoanSerializer


class OfferViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = models.Product.objects.all()
    serializer_class = serializers.OfferSerializer


class AfterMaturityViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = models.Product.objects.all()
    serializer_class = serializers.AfterMaturitySerialzier
