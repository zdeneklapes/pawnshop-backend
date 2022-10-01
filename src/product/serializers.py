from rest_framework import serializers

from . import models


class ProductSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    buy_price = serializers.IntegerField(required=False)
    sell_price = serializers.IntegerField(required=False)

    class Meta:
        model = models.Product
        fields = '__all__' #["date_extended_deadline","date_end"]
