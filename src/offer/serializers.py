from rest_framework import serializers

from . import models


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Offer
        fields = "__all__"
