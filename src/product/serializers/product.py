from django.utils import timezone
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from customer.serializers import CustomerProfileSerializer
from product.models import Product, ProductStatusOrData
from common import utils
from config.settings import AUTH
from authentication.models.models import User


class ProductSerializer(WritableNestedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
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

        if attrs["status"] in [ProductStatusOrData.OFFER.name]:
            if not utils.is_integer(attrs["interest_rate_or_quantity"]):
                raise serializers.ValidationError({"interest_rate_or_quantity": "Must be integer"})

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
        sell_price = (
            data["sell_price"]
            if data["status"] == ProductStatusOrData.OFFER.name
            else utils.get_sell_price(rate=float(data["interest_rate_or_quantity"]), buy_price=int(data["buy_price"]))
        )

        data.update(
            {
                "user": 1 if not AUTH else self.context["request"].user.id,
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
                "sell_price": sell_price,
                "date_extend": timezone.now(),
                "quantity": data["interest_rate_or_quantity"]
                if data["status"] == ProductStatusOrData.OFFER.name
                else 1,
            }
        )
        return super().to_internal_value(data)
