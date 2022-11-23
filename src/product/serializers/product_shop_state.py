from rest_framework import serializers


class ProductShopStateSerializer(serializers.Serializer):
    status = serializers.CharField()
    count = serializers.IntegerField()
    buy = serializers.IntegerField()
    sell = serializers.IntegerField()
