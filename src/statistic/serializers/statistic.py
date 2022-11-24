from typing import Tuple, Literal, Optional

from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework.request import Request

from statistic.models import Statistic
from statistic.models.choices import StatisticQueryParams, StatisticDescription
from common.exceptions import BadQueryParam
from config.settings import AUTH
from product.models.choices import ProductStatusOrData


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

    # ###########################################################################################
    # Validate
    # ###########################################################################################
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

    # ###########################################################################################
    # Save Helpers
    # ###########################################################################################
    @staticmethod
    def save_statistic_auth_create(
        operation: Literal[StatisticDescription.LOGIN, StatisticDescription.LOGOUT], user_id
    ) -> None:
        StatisticSerializer.save_statistics(operation=operation, user=1 if not AUTH else user_id)

    @staticmethod
    def save_statistic_product_update(request: Request, buy_price_prev: int, sell_price_prev: int) -> None:
        operation, price = StatisticSerializer.validate_operation(request, buy_price_prev, sell_price_prev)

        StatisticSerializer.save_statistics(
            operation=operation,
            user=1 if not AUTH else request.user.id,
            price=price,
            product=request.parser_context["kwargs"]["pk"],
        )

    @staticmethod
    def save_statistic_product_create(request, response) -> None:
        StatisticSerializer.save_statistics(
            operation=StatisticDescription.LOAN_CREATE.name
            if request.data["status"] == ProductStatusOrData.LOAN.name
            else StatisticDescription.OFFER_BUY.name,
            user=1 if not AUTH else request.user.id,
            price=-response.data["buy_price"],
            product=response.data["id"],
        )

    @staticmethod
    def save_statistics(operation: str, user: int, price: Optional[int] = None, product: Optional[int] = None) -> None:
        serializer_stats = StatisticSerializer(
            data={"description": operation, "price": price, "product": product, "user": user}
        )
        if not serializer_stats.is_valid():
            raise serializers.ValidationError(serializer_stats.errors)
        serializer_stats.save()

    # ###########################################################################################
    # Inherited
    # ###########################################################################################
    def to_internal_value(self, data):
        var_search = "update"

        if var_search not in data:
            return super().to_internal_value(data)

        if data["update"] in [StatisticQueryParams.RESET.name]:
            data.update(
                {
                    "user": 1 if not AUTH else self.context["request"].user.id,
                    "description": StatisticQueryParams.RESET.name,
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
