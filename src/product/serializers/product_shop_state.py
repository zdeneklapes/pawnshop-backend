from rest_framework import serializers

from product.models import Product


class ProductShopStateSerializer(serializers.ModelSerializer):
    status = serializers.CharField()
    # status = serializers.ChoiceField(
    #     source="get_description_display", choices=ProductStatusOrData, read_only=True
    # )
    count = serializers.IntegerField()
    buy = serializers.IntegerField()
    sell = serializers.IntegerField()

    class Meta:
        model = Product
        fields = ["status", "count", "buy", "sell"]
