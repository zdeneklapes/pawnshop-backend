import datetime

from django.utils import timezone
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from common import utils
from product.models import Product, ProductStatusOrData
from statistic.models import StatisticDescription
from authentication.models.choices import UserGroupChoice


class ProductUpdateSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    # ######################################################################
    # Validate
    # ######################################################################
    def validate_update_loan(self):
        if self.context["request"].data["update"] in [
            StatisticDescription.LOAN_EXTEND.name,
            StatisticDescription.LOAN_RETURN.name,
            StatisticDescription.UPDATE_DATA.name,
        ]:
            return None
        else:
            raise serializers.ValidationError(
                {"update": f"Bad update request for status product: {ProductStatusOrData.LOAN.name}"}
            )

    def validate_update_offer(self):
        if self.context["request"].data["update"] in [StatisticDescription.OFFER_SELL.name]:
            if self.context["request"].data["quantity"] > self.instance.interest_rate_or_quantity:
                raise serializers.ValidationError(
                    {
                        "quantity": f"You can sell only only available quantity. "
                        f"Available: {self.instance.interest_rate_or_quantity}"
                    }
                )
            return None

        if self.context["request"].data["update"] in [StatisticDescription.UPDATE_DATA.name]:
            return None

        if self.context["request"].data["update"] in [StatisticDescription.OFFER_BUY.name]:
            return None

        raise serializers.ValidationError(
            {"update": f"Bad update request for status product: {ProductStatusOrData.OFFER.name}"}
        )

    def validate_update_after_maturity(self):
        if self.context["request"].data["update"] in [
            StatisticDescription.LOAN_EXTEND.name,
            StatisticDescription.LOAN_RETURN.name,
            StatisticDescription.LOAN_TO_OFFER.name,
            StatisticDescription.UPDATE_DATA.name,
        ]:
            return None
        else:
            raise serializers.ValidationError(
                {"update": f"Bad update request for status product: {ProductStatusOrData.AFTER_MATURITY.name}"}
            )

    def validate(self, attrs):
        if self.instance.status in [ProductStatusOrData.AFTER_MATURITY.name]:
            self.validate_update_after_maturity()

        if self.instance.status in [ProductStatusOrData.LOAN.name]:
            self.validate_update_loan()

        if self.instance.status in [ProductStatusOrData.OFFER.name]:
            self.validate_update_offer()

        return super().validate(attrs)

    # ######################################################################
    # Set data
    # ######################################################################
    def set_data_loan_return(self) -> dict:
        product = Product.objects.get(id=self.context["view"].kwargs["pk"])
        return {
            "status": ProductStatusOrData.INACTIVE_LOAN.name,
            "sell_price": product.sell_price,
            "date_extend": product.date_extend,
            "date_end": timezone.now(),
            "interest_rate_or_quantity": product.interest_rate_or_quantity,
        }

    def set_data_loan_extend(self) -> dict:
        product = Product.objects.get(id=self.context["view"].kwargs["pk"])
        return {
            "status": ProductStatusOrData.LOAN.name,
            "sell_price": utils.get_sell_price(rate=product.interest_rate_or_quantity, buy_price=product.buy_price),
            "date_extend": timezone.now(),
            "date_end": timezone.now() + datetime.timedelta(weeks=product.rate_times),
            "interest_rate_or_quantity": product.interest_rate_or_quantity,
        }

    def set_data_loan_to_offer(self, data) -> dict:
        product = Product.objects.get(id=self.context["view"].kwargs["pk"])
        data.update(
            {
                "status": ProductStatusOrData.OFFER.name,
                "sell_price": data["sell_price"],
                "date_extend": product.date_extend,
                "date_end": timezone.now(),
                "interest_rate_or_quantity": 1,
            }
        )
        return data

    def set_data_offer_sell(self, data: dict):
        product = Product.objects.get(id=self.context["view"].kwargs["pk"])
        _data = {
            "status": (
                ProductStatusOrData.INACTIVE_OFFER.name
                if product.interest_rate_or_quantity - data["quantity"] <= 0
                else ProductStatusOrData.OFFER.name
            ),
            "sell_price": product.sell_price,
            "date_extend": product.date_extend,
            "date_end": product.date_end,
            "interest_rate_or_quantity": product.interest_rate_or_quantity - data["quantity"],
        }
        return _data

    def set_data_offer_buy(self, data: dict) -> dict:
        product = Product.objects.get(id=self.context["view"].kwargs["pk"])
        data.update(
            {
                "status": ProductStatusOrData.OFFER.name,
                "sell_price": product.sell_price,
                "date_extend": product.date_extend,
                "date_end": product.date_end,
                "interest_rate_or_quantity": product.interest_rate_or_quantity + data["quantity"],
            }
        )
        return data

    def set_data_update_loan(self, data: dict) -> dict:
        if self.context["request"].user.role == UserGroupChoice.ADMIN.name:
            return {
                "update": data["update"],
                "product_name": data["product_name"],
                "inventory_id": data["inventory_id"],
                # "sell_price": data["sell_price"],
                "date_create": data["date_create"],
                "date_extend": data["date_extend"],
            }

        if self.context["request"].user.role == UserGroupChoice.ATTENDANT.name:
            return {
                "update": data["update"],
                "product_name": data["product_name"],
                "inventory_id": data["inventory_id"],
            }

        raise serializers.ValidationError({"error": "You don't have permission to update this product"})

    def set_data_update_offer(self, data: dict) -> dict:
        if self.context["request"].user.role == UserGroupChoice.ADMIN.name:
            return {
                "update": data["update"],
                "product_name": data["product_name"],
                "inventory_id": data["inventory_id"],
                "sell_price": data["sell_price"],
                "date_create": data["date_create"],
                "date_extend": data["date_extend"],
            }

        if self.context["request"].user.role == UserGroupChoice.ATTENDANT.name:
            return {
                "update": data["update"],
                "product_name": data["product_name"],
                "inventory_id": data["inventory_id"],
                "sell_price": data["sell_price"],
            }

        raise serializers.ValidationError({"error": "You don't have permission to update this product"})

    def set_data_update(self, data: dict) -> dict:
        product = Product.objects.get(id=self.context["view"].kwargs["pk"])

        if product.status == ProductStatusOrData.LOAN.name:
            return self.set_data_update_loan(data)
        if product.status == ProductStatusOrData.OFFER.name:
            return self.set_data_update_offer(data)

        raise serializers.ValidationError({"error": "You can't update this product"})

    # ######################################################################
    # Inherited methods
    # ######################################################################
    def to_representation(self, instance):
        dict_ = super().to_representation(instance)
        dict_["interest"] = utils.get_interests(
            rate=float(instance.interest_rate_or_quantity),
            buy_price=instance.buy_price,
            from_date=instance.date_extend.date(),
        )
        return dict_

    def to_internal_value(self, data):
        if data["update"] == StatisticDescription.LOAN_RETURN.name:
            return super(ProductUpdateSerializer, self).to_internal_value(self.set_data_loan_return())
        if data["update"] == StatisticDescription.LOAN_EXTEND.name:
            return super().to_internal_value(self.set_data_loan_extend())
        if data["update"] == StatisticDescription.LOAN_TO_OFFER.name:
            return super().to_internal_value(self.set_data_loan_to_offer(data))
        if data["update"] == StatisticDescription.OFFER_SELL.name:
            return super().to_internal_value(self.set_data_offer_sell(data))
        if data["update"] == StatisticDescription.OFFER_BUY.name:
            return super().to_internal_value(self.set_data_offer_buy(data))
        if data["update"] == StatisticDescription.UPDATE_DATA:
            return super().to_internal_value(self.set_data_update(data))

        raise serializers.ValidationError("Invalid update")
