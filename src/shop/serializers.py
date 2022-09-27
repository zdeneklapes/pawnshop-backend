from rest_framework import serializers

from . import models


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Shop
        fields = "__all__"

    def create(self, validated_data):
        return models.Shop.objects.create(**validated_data)
