from rest_framework import serializers


class ProductShopStateSerializer(serializers.Serializer):
    status = serializers.CharField()
    # status = serializers.ChoiceField(
    #     source="get_status_display", choices=ProductStatusOrData, read_only=True
    # )
    count = serializers.IntegerField()
    buy = serializers.IntegerField()
    sell = serializers.IntegerField()

    class Meta:
        fields = ["status", "count", "buy", "sell"]
