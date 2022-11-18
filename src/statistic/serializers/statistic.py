from typing import Tuple

from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework.request import Request

from statistic.models import Statistic
from statistic.models.choices import StatisticQPData, StatisticDescription
from common.exceptions import BadQueryParam
from config.settings import AUTH


class StatisticAllSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(required=False, read_only=True)
    profit = serializers.IntegerField(required=False, read_only=True)
    username = serializers.CharField(source="user.email", read_only=True)
    description = serializers.ChoiceField(
        source="get_description_display", choices=StatisticDescription, read_only=True
    )

    class Meta:
        model = Statistic
        fields = ["id", "amount", "profit", "datetime", "description", "price", "product", "username", "user"]


class StatisticSerializer(WritableNestedModelSerializer):
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
            elif operation == StatisticDescription.LOAN_CREATE.name:  # pylint: disable=E1101
                price = -buy_price_prev
            elif operation == StatisticDescription.LOAN_RETURN.name:  # pylint: disable=E1101
                price = sell_price_prev
            elif operation == StatisticDescription.LOAN_TO_OFFER.name:  # pylint: disable=E1101
                price = 0
            elif operation == StatisticDescription.OFFER_SELL.name:  # pylint: disable=E1101
                price = request.data["quantity"] * sell_price_prev
            elif operation == StatisticDescription.OFFER_BUY.name:  # pylint: disable=E1101
                price = -request.data["quantity"] * buy_price_prev
            elif operation == StatisticDescription.UPDATE_DATA.name:  # pylint: disable=E1101
                price = 0
            else:
                raise BadQueryParam()
        return operation, price

    @staticmethod
    def validate_and_save(request: Request, buy_price_prev: int, sell_price_prev: int) -> None:
        # Validate
        operation, price = StatisticSerializer.validate_operation(request, buy_price_prev, sell_price_prev)

        # Save Statistics
        StatisticSerializer.save_statistics(
            price=price,
            operation=operation,
            user=1 if not AUTH else request.user.id,
            product=request.parser_context["kwargs"]["pk"],
        )

    @staticmethod
    def save_statistics(price: int, operation: str, user: int, product: int = None) -> None:
        serializer_stats = StatisticSerializer(
            data={"description": operation, "price": price, "product": product, "user": user}
        )
        serializer_stats.is_valid()
        serializer_stats.save()

    def to_internal_value(self, data):
        var_search = "update"

        if var_search not in data:
            return super().to_internal_value(data)

        if data["update"] in [StatisticQPData.RESET.name]:
            data.update(
                {
                    "user": 1 if not AUTH else self.context["request"].user.id,
                    "description": StatisticQPData.RESET.name,
                }
            )
            return super().to_internal_value(data)

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
