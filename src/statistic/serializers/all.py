from rest_framework import serializers

from statistic.models import StatisticDescription, Statistic


class StatisticAllSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(required=False, read_only=True)
    profit = serializers.IntegerField(required=False, read_only=True)

    username = serializers.CharField(source="user.email", read_only=True)
    product_name = serializers.CharField(
        source="product.product_name", read_only=True, allow_null=True
    )  # allow_null dont remove null keys:values pairs
    description = serializers.ChoiceField(
        source="get_description_display", choices=StatisticDescription, read_only=True
    )

    class Meta:
        model = Statistic
        fields = ["datetime", "description", "price", "product", "username", "product_name", "amount", "profit"]
