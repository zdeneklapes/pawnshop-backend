import datetime

from django.utils import timezone
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from customer.serializers import CustomerProfileSerializer
from product.models import Product, ProductStatus
from common import utils


def get_interests(rate: float, buy_price: int, rate_times: int):
    return [
        {
            "from": datetime.date.today() + datetime.timedelta(weeks=i),
            "to": datetime.date.today() + datetime.timedelta(weeks=i + 1),
            "price": utils.get_sell_price(rate, buy_price, i + 1),
        }
        for i in range(rate_times)
    ]


class ProductSerializer(WritableNestedModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(U)
    customer = CustomerProfileSerializer()
    sell_price = serializers.IntegerField(required=False)

    class Meta:
        model = Product
        fields = "__all__"

    def to_representation(self, instance):
        dict_ = super().to_representation(instance)
        del dict_["interest_rate"]
        del dict_["quantity"]
        del dict_["rate_frequency"]
        del dict_["rate_times"]
        if instance.status == ProductStatus.LOAN.name:
            dict_["interest_rate_or_quantity"] = (
                instance.interest_rate if instance.status == ProductStatus.LOAN.name else instance.quantity
            )
            dict_["interest"] = get_interests(
                rate=float(instance.interest_rate), buy_price=instance.buy_price, rate_times=instance.rate_times
            )
            return dict_
        else:
            return super(ProductSerializer, self).to_representation(instance)

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
                "interest_rate": data["interest_rate_or_quantity"]
                if data["status"] == ProductStatus.LOAN.name
                else None,
                "product_name": data["product_name"],
                "buy_price": data["buy_price"],
                "sell_price": utils.get_sell_price(
                    rate=float(data["interest_rate_or_quantity"]), buy_price=int(data["buy_price"])
                ),
                "date_extend": timezone.now(),
                "quantity": data["interest_rate_or_quantity"] if data["status"] == ProductStatus.OFFER.name else 1,
            }
        )
        return super().to_internal_value(data)


class LoanExtendSerializer(WritableNestedModelSerializer):
    customer = CustomerProfileSerializer()
    sell_price = serializers.IntegerField(required=False)

    class Meta:
        model = Product
        fields = "__all__"

    def to_representation(self, instance):
        dict_ = super().to_representation(instance)
        dict_["interest"] = get_interests(
            rate=float(instance.rate), buy_price=instance.buy_price, rate_times=instance.rate_times
        )
        return dict_

    def to_internal_value(self, data):
        loan = Product.objects.get(id=self.context["view"].kwargs["pk"])
        data.update(
            {
                "status": ProductStatus.LOAN.name,
                "sell_price": utils.get_sell_price(rate=loan.rate, buy_price=loan.buy_price),
                "date_extend": timezone.now(),
            }
        )
        return super().to_internal_value(data)


class LoanReturnSerializer(WritableNestedModelSerializer):
    customer = CustomerProfileSerializer()
    sell_price = serializers.IntegerField(required=False)

    class Meta:
        model = Product
        fields = "__all__"

    def to_internal_value(self, data):
        data.update(
            {
                "status": ProductStatus.INACTIVE_LOAN.name,
                "date_end": timezone.now()
                # "sell_price": "" # Note: Is already set from command
            }
        )
        return super().to_internal_value(data)


class LoanToOfferSerializer(WritableNestedModelSerializer):
    customer = CustomerProfileSerializer()
    sell_price = serializers.IntegerField(required=False)

    class Meta:
        model = Product
        fields = "__all__"

    def to_internal_value(self, data):
        data.update({"status": ProductStatus.OFFER.name, "sell_price": data["sell_price"]})
        return super().to_internal_value(data)


class ShopStateSerializer(serializers.Serializer):
    status = serializers.CharField()
    count = serializers.IntegerField()
    buy = serializers.IntegerField()
    sell = serializers.IntegerField()


class OfferSellSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Product
        fields = ["status", "sell_price"]

    def to_internal_value(self, data):
        product = Product.objects.get(id=self.context["view"].kwargs["pk"])
        data.update({"status": ProductStatus.INACTIVE_OFFER.name, "sell_price": product.sell_price})
        return super().to_internal_value(data)


class UpdateProductSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Product
        fields = ["product_name", "sell_price", "date_create", "date_extend", "inventory_id"]

    def to_internal_value(self, data):
        data.update(
            {
                "product_name": data["product_name"],
                "sell_price": data["sell_price"],
                "date_create": data["date_create"],
                "date_extend": data["date_extend"],
                "inventory_id": data["inventory_id"],
            }
        )
        return super().to_internal_value(data)
