from rest_framework import viewsets

from . import models, serializers


class OfferViewSet(viewsets.ModelViewSet):
    queryset = models.Offer.objects.all()
    serializer_class = serializers.OfferSerializer
