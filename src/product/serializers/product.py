import datetime

from django.utils import timezone
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from customer.serializers import CustomerProfileSerializer

from product.models import models
from common import utils
from product.models import choices


def get_interests(rate: float, buy_price: int, rate_times: int):
    return [
        {
            "from": datetime.date.today() + datetime.timedelta(weeks=i),
            "to": datetime.date.today() + datetime.timedelta(weeks=i + 1),
            "price": utils.get_sell_price(rate, buy_price, i + 1),
        }
        for i in range(rate_times)
    ]


class CreateProductSerializer(WritableNestedModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(U)
    customer = CustomerProfileSerializer()
    sell_price = serializers.IntegerField(required=False)

    class Meta:
        model = models.Product
        fields = "__all__"

    def to_representation(self, instance):
        if instance.status == choices.ProductStatus.LOAN.name:
            dict_ = super().to_representation(instance)
            dict_["interest"] = get_interests(
                rate=float(instance.rate), buy_price=instance.buy_price, rate_times=instance.rate_times
            )
            return dict_
        else:
            return super(CreateProductSerializer, self).to_representation(instance)

    def to_internal_value(self, data):
        data.update(
            {
                "user": data["user"],
                "customer": {
                    "id_birth": data["id_birth"],
                    "full_name": data["full_name"],
                    "personal_id": data["personal_id"],
                    "personal_id_expiration_date": data["personal_id_expiration_date"],
                    "residence": data["residence"],
                    "nationality": data["nationality"],
                    "birthplace": data["birthplace"],
                    "sex": data["sex"],
                },
                "status": data["status"],
                "inventory_id": data["inventory_id"],
                "rate": data["interest_rate_or_quantity"]
                if data["status"] == choices.ProductStatus.LOAN.name
                else None,
                "product_name": data["product_name"],
                "buy_price": data["buy_price"],
                "sell_price": utils.get_sell_price(
                    rate=float(data["interest_rate_or_quantity"]), buy_price=int(data["buy_price"])
                ),
                "date_extend": timezone.now(),
                "quantity": data["interest_rate_or_quantity"]
                if data["status"] == choices.ProductStatus.OFFER.name
                else 1,
            }
        )
        return super().to_internal_value(data)


class LoanExtendSerializer(WritableNestedModelSerializer):
    customer = CustomerProfileSerializer()
    sell_price = serializers.IntegerField(required=False)

    class Meta:
        model = models.Product
        fields = "__all__"

    def to_representation(self, instance):
        dict_ = super().to_representation(instance)
        dict_["interest"] = get_interests(
            rate=float(instance.rate), buy_price=instance.buy_price, rate_times=instance.rate_times
        )
        return dict_

    def to_internal_value(self, data):
        loan = models.Product.objects.get(id=self.context["view"].kwargs["pk"])
        data.update(
            {
                "status": models.ProductStatus.LOAN.name,
                "sell_price": utils.get_sell_price(rate=loan.rate, buy_price=loan.buy_price),
                "date_extend": timezone.now(),
            }
        )
        return super().to_internal_value(data)


class LoanReturnSerializer(WritableNestedModelSerializer):
    customer = CustomerProfileSerializer()
    sell_price = serializers.IntegerField(required=False)

    class Meta:
        model = models.Product
        fields = "__all__"

    def to_internal_value(self, data):
        data.update(
            {
                "status": choices.ProductStatus.INACTIVE_LOAN.name,
                "date_end": timezone.now()
                # "sell_price": "" # Note: Is already set from command
            }
        )
        return super().to_internal_value(data)


class LoanToOfferSerializer(WritableNestedModelSerializer):
    customer = CustomerProfileSerializer()
    sell_price = serializers.IntegerField(required=False)

    class Meta:
        model = models.Product
        fields = "__all__"

    def to_internal_value(self, data):
        data.update({"status": choices.ProductStatus.OFFER.name, "sell_price": data["sell_price"]})
        return super().to_internal_value(data)


class ShopStateSerializer(serializers.Serializer):
    status = serializers.CharField()
    count = serializers.IntegerField()
