from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from statistic.models import models
from statistic.utils.choices import StatisticQueryParamsChoices


class StatisticDefaultSerializer(WritableNestedModelSerializer):
    amount = serializers.IntegerField(required=False, read_only=True)
    profit = serializers.IntegerField(required=False, read_only=True)

    class Meta:
        model = models.Statistic
        fields = "__all__"

    @classmethod
    def save_statistics(self, price: int, operation: str, user: int, product: int = None) -> None:
        serializer_stats = StatisticDefaultSerializer(
            data={"description": operation, "price": price, "product": product, "user": user}
        )
        serializer_stats.is_valid()
        serializer_stats.save()


class StatisticDailyStatsSerializer(serializers.Serializer):
    pass


class StatisticCashAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Statistic
        fields = ["amount"]


class StatisticShopStateSerializer(serializers.Serializer):
    pass


class StatisticResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Statistic
        fields = ["user", "description"]

    def to_internal_value(self, data):
        data.update(
            {
                "user": 1,  # TODO: Change to - self.request.user.id
                "description": StatisticQueryParamsChoices.RESET.name,
            }
        )
        return super().to_internal_value(data)
