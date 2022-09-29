from rest_framework import serializers

from . import models


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Shop
        fields = "__all__"

    def create(self, validated_data):
        shop = super().create(validated_data)
        shop.save()
        return shop

    def update(self, instance, validated_data):
        shop = super().update(instance, validated_data)
        return shop
