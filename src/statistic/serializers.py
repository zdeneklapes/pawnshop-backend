from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from .models import models


class StatisticSerializer(WritableNestedModelSerializer):
    amount = serializers.IntegerField(required=False, read_only=True)
    profit = serializers.IntegerField(required=False, read_only=True)

    class Meta:
        model = models.Statistic
        fields = "__all__"

    @classmethod
    def save_statistics(self, price: int, operation: str, user: int, product: int = None) -> None:
        serializer_stats = StatisticSerializer(
            data={"description": operation, "price": price, "product": product, "user": user}
        )
        serializer_stats.is_valid()
        serializer_stats.save()


class StatisticResetSerializer(WritableNestedModelSerializer):
    amount = serializers.IntegerField(required=False, read_only=True)

    class Meta:
        model = models.Statistic
        fields = "__all__"

    def to_internal_value(self, data):
        # prev_statistic = models.Statistic.objects.last()
        data.update(
            {
                # "status": models.ProductStatus.LOAN.name,
                # "sell_price": utils.get_sell_price(rate=loan.rate, buy_price=loan.buy_price),
                # "date_extend": timezone.now(),
            }
        )
        return super().to_internal_value(data)


class StatisticCashAmountSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
