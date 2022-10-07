from typing import Tuple

from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework.request import Request

from statistic.models import Statistic
from statistic.models.choices import StatisticQPData, StatisticDescription
from common.exceptions import BadQueryParam


class StatisticDefaultSerializer(WritableNestedModelSerializer):
    amount = serializers.IntegerField(required=False, read_only=True)
    profit = serializers.IntegerField(required=False, read_only=True)

    class Meta:
        model = Statistic
        fields = "__all__"

    @staticmethod
    def validate_operation(request: Request, buy_price_prev: int, sell_price_prev: int) -> Tuple[str, int]:
        var_search = "update"

        if var_search not in request.data:
            raise BadQueryParam()
        else:
            operation = request.data[var_search]
            if operation == StatisticDescription.LOAN_EXTEND.name:  # pylint: disable=E1101
                price = sell_price_prev - buy_price_prev
            elif operation == StatisticDescription.LOAN_RETURN.name:  # pylint: disable=E1101
                price = sell_price_prev
            elif operation == StatisticDescription.LOAN_TO_OFFER.name:  # pylint: disable=E1101
                price = 0
            elif operation == StatisticDescription.OFFER_SELL.name:  # pylint: disable=E1101
                price = request.data["quantity"] * sell_price_prev
            elif operation == StatisticDescription.OFFER_BUY.name:  # pylint: disable=E1101
                price = request.data["quantity"] * buy_price_prev
            elif operation == StatisticDescription.UPDATE_DATA.name:  # pylint: disable=E1101
                price = 0
            else:
                raise BadQueryParam()
        return operation, price

    @staticmethod
    def validate_and_save(request: Request, buy_price_prev: int, sell_price_prev: int) -> None:
        # Validate
        operation, price = StatisticDefaultSerializer.validate_operation(request, buy_price_prev, sell_price_prev)

        # Save Statistics
        StatisticDefaultSerializer.save_statistics(
            price=price,
            operation=operation,
            user=request.user.id,
            product=request.parser_context["kwargs"]["pk"],
        )

    @staticmethod
    def save_statistics(price: int, operation: str, user: int, product: int = None) -> None:
        serializer_stats = StatisticDefaultSerializer(
            data={"description": operation, "price": price, "product": product, "user": 1}  # TODO: user
        )
        serializer_stats.is_valid()
        serializer_stats.save()

    def to_internal_value(self, data):
        data.update(
            {
                "user": 1,  # TODO: Change to - self.request.user.id
                "description": StatisticQPData.RESET.name,
            }
        )
        return super().to_internal_value(data)


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
        model = Statistic
        fields = ["amount"]


class StatisticResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        fields = ["user", "description"]

    def to_internal_value(self, data):
        data.update(
            {
                "user": 1,  # TODO: Change to - self.request.user.id
                "description": StatisticQPData.RESET.name,
            }
        )
        return super().to_internal_value(data)
