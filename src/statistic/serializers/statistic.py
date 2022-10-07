from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from statistic.models import models
from statistic.models.choices import StatisticQPData


class StatisticDefaultSerializer(WritableNestedModelSerializer):
    amount = serializers.IntegerField(required=False, read_only=True)
    profit = serializers.IntegerField(required=False, read_only=True)

    class Meta:
        model = models.Statistic
        fields = "__all__"

    @classmethod
    def save_statistics(self, price: int, operation: str, user: int, product: int = None) -> None:
        serializer_stats = StatisticDefaultSerializer(
            data={"description": operation, "price": price, "product": product, "user": 1}  # TODO: user
        )
        serializer_stats.is_valid()
        serializer_stats.save()


class StatisticDailyStatsSerializer(serializers.Serializer):
    date = serializers.DateField()
    loan_create_count = serializers.IntegerField()
    loan_extend_count = serializers.IntegerField()
    loan_return_count = serializers.IntegerField()
    loan_income = serializers.IntegerField()
    loan_outcome = serializers.IntegerField()
    loan_profit = serializers.IntegerField()
    #
    offer_create_count = serializers.IntegerField()
    offer_sell_count = serializers.IntegerField()
    offer_income = serializers.IntegerField()
    offer_outcome = serializers.IntegerField()
    offer_profit = serializers.IntegerField()
    #
    all_income = serializers.IntegerField()
    all_outcome = serializers.IntegerField()
    all_profit = serializers.IntegerField()


class StatisticCashAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Statistic
        fields = ["amount"]


class StatisticResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Statistic
        fields = ["user", "description"]

    def to_internal_value(self, data):
        data.update(
            {
                "user": 1,  # TODO: Change to - self.request.user.id
                "description": StatisticQPData.RESET.name,
            }
        )
        return super().to_internal_value(data)
