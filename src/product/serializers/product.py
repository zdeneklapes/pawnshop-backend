import datetime

from django.utils import timezone
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from customer.serializers import CustomerProfileSerializer
from product.models import Product, ProductStatusOrData
from common import utils
from statistic.models.choices import StatisticDescription


class ProductSerializer(WritableNestedModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(U)
    customer = CustomerProfileSerializer()
    sell_price = serializers.IntegerField(required=False)

    class Meta:
        model = Product
        fields = "__all__"

    def validate(self, attrs):
        if attrs["status"] not in [ProductStatusOrData.LOAN.name, ProductStatusOrData.OFFER.name]:
            raise serializers.ValidationError(
                {
                    "status": f"Creating product must have status set to: "
                    f"{ProductStatusOrData.OFFER.name} or {ProductStatusOrData.LOAN.name}"
                }
            )
        return super().validate(attrs)

    def to_representation(self, instance):
        dict_ = super().to_representation(instance)
        del dict_["rate_frequency"]
        del dict_["rate_times"]
        if instance.status in [ProductStatusOrData.LOAN.name, ProductStatusOrData.AFTER_MATURITY.name]:
            dict_["interest"] = utils.get_interests(
                rate=float(instance.interest_rate_or_quantity),
                buy_price=instance.buy_price,
                from_date=instance.date_extend.date(),
            )

        return dict_

    def to_internal_value(self, data):
        data.update(
            {
                "user": data["user"],  # TODO: Change to - data.user.id
                "customer": {
                    "id_birth": data["customer"]["id_birth"],
                    "full_name": data["customer"]["full_name"],
                    "personal_id": data["customer"]["personal_id"],
                    "personal_id_expiration_date": data["customer"]["personal_id_expiration_date"],
                    "residence": data["customer"]["residence"],
                    "nationality": data["customer"]["nationality"],
                    "birthplace": data["customer"]["birthplace"],
                    "sex": data["customer"]["sex"],
                },
                "status": data["status"],
                "inventory_id": data["inventory_id"],
                "interest_rate_or_quantity": data["interest_rate_or_quantity"],
                "product_name": data["product_name"],
                "buy_price": data["buy_price"],
                "sell_price": utils.get_sell_price(
                    rate=float(data["interest_rate_or_quantity"]), buy_price=int(data["buy_price"])
                ),
                "date_extend": timezone.now(),
                "quantity": data["interest_rate_or_quantity"]
                if data["status"] == ProductStatusOrData.OFFER.name
                else 1,
            }
        )
        return super().to_internal_value(data)


class ProductUpdateSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def validate_update_loan(self):
        if self.context["request"].data["update"] in [
            StatisticDescription.LOAN_EXTEND.name,
            StatisticDescription.LOAN_RETURN.name,
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
        if self.context["request"].data["update"] in [StatisticDescription.OFFER_BUY.name]:
            return None
        else:
            raise serializers.ValidationError(
                {"update": f"Bad update request for status product: {ProductStatusOrData.OFFER.name}"}
            )

    def validate_update_after_maturity(self):
        if self.context["request"].data["update"] in [
            StatisticDescription.LOAN_EXTEND.name,
            StatisticDescription.LOAN_RETURN.name,
            StatisticDescription.LOAN_TO_OFFER.name,
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

    def get_status(self, data, product):
        map_ = {
            StatisticDescription.LOAN_RETURN.name: ProductStatusOrData.INACTIVE_LOAN.name,
            StatisticDescription.LOAN_EXTEND.name: ProductStatusOrData.LOAN.name,
            StatisticDescription.LOAN_TO_OFFER.name: ProductStatusOrData.OFFER.name,
            StatisticDescription.OFFER_SELL.name: ProductStatusOrData.INACTIVE_OFFER.name
            if self.get_interest_rate_or_quantity(data, product) <= 0
            else ProductStatusOrData.OFFER.name,
            StatisticDescription.OFFER_BUY.name: ProductStatusOrData.OFFER.name,
        }
        return map_[data["update"]]

    def get_sell_price(self, data, product):
        map_ = {
            StatisticDescription.LOAN_RETURN.name: product.sell_price,
            StatisticDescription.LOAN_EXTEND.name: utils.get_sell_price(
                rate=product.interest_rate_or_quantity, buy_price=product.buy_price
            ),
            StatisticDescription.OFFER_SELL.name: product.sell_price,
            StatisticDescription.OFFER_BUY.name: product.sell_price,
        }

        if StatisticDescription.LOAN_TO_OFFER.name == data["update"]:
            return data["sell_price"]

        return map_[data["update"]]

    def get_date_extend(self, data, product):
        map_ = {
            StatisticDescription.LOAN_RETURN.name: product.date_extend,
            StatisticDescription.LOAN_EXTEND.name: timezone.now(),
            StatisticDescription.LOAN_TO_OFFER.name: product.date_extend,
            StatisticDescription.OFFER_SELL.name: product.date_extend,
            StatisticDescription.OFFER_BUY.name: product.date_extend,
        }
        return map_[data["update"]]

    def get_date_end(self, data, product):
        map_ = {
            StatisticDescription.LOAN_RETURN.name: timezone.now(),
            StatisticDescription.LOAN_EXTEND.name: timezone.now() + datetime.timedelta(weeks=product.rate_times),
            StatisticDescription.LOAN_TO_OFFER.name: timezone.now(),
            StatisticDescription.OFFER_SELL.name: product.date_end,
            StatisticDescription.OFFER_BUY.name: product.date_end,
        }
        return map_[data["update"]]

    def get_interest_rate_or_quantity(self, data, product):
        map_ = {
            StatisticDescription.LOAN_RETURN.name: product.interest_rate_or_quantity,
            StatisticDescription.LOAN_EXTEND.name: product.interest_rate_or_quantity,
            StatisticDescription.LOAN_TO_OFFER.name: 1,
        }

        if data["update"] in [StatisticDescription.OFFER_SELL.name, StatisticDescription.OFFER_BUY.name]:
            map_ = {
                StatisticDescription.OFFER_SELL.name: product.interest_rate_or_quantity - data["quantity"],
                StatisticDescription.OFFER_BUY.name: product.interest_rate_or_quantity + data["quantity"],
            }

        return map_[data["update"]]

    #
    def to_representation(self, instance):
        dict_ = super().to_representation(instance)
        dict_["interest"] = utils.get_interests(
            rate=float(instance.interest_rate_or_quantity),
            buy_price=instance.buy_price,
            from_date=instance.date_extend.date(),
        )
        return dict_

    def to_internal_value(self, data):
        product = Product.objects.get(id=self.context["view"].kwargs["pk"])

        if data["update"] in [
            StatisticDescription.LOAN_RETURN.name,
            StatisticDescription.LOAN_EXTEND.name,
            StatisticDescription.LOAN_TO_OFFER.name,
            StatisticDescription.OFFER_SELL.name,
            StatisticDescription.OFFER_BUY.name,
        ]:
            data.update(
                {
                    "status": self.get_status(data, product),
                    "sell_price": self.get_sell_price(data, product),
                    "date_extend": self.get_date_extend(data, product),
                    "date_end": self.get_date_end(data, product),
                    "interest_rate_or_quantity": self.get_interest_rate_or_quantity(data, product),
                }
            )
        elif data["update"] in [StatisticDescription.UPDATE_DATA]:
            # Here will be updated data
            pass

        return super().to_internal_value(data)


class ProductShopStateSerializer(serializers.Serializer):
    status = serializers.CharField()
    count = serializers.IntegerField()
    buy = serializers.IntegerField()
    sell = serializers.IntegerField()
