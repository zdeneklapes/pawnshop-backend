from rest_framework import viewsets, mixins, permissions

from . import models, serializers


class OfferViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Offer.objects.all()
    serializer_class = serializers.OfferSerializer
    permission_classes = [permissions.IsAuthenticated]
