import datetime

from django.utils import timezone
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from authentication.serializers import CustomerProfileSerializer

from .models import models
from common import utils


class ProductSerializer(WritableNestedModelSerializer):
    customer = CustomerProfileSerializer()
    sell_price = serializers.IntegerField(required=False)

    class Meta:
        model = models.Product
        fields = "__all__"

    def add_interests(self, data):
        data["interest"] = [
            {
                "from": datetime.date.today() + datetime.timedelta(weeks=i),
                "to": datetime.date.today() + datetime.timedelta(weeks=i + 1),
                "price": utils.get_sell_price(float(data["rate"]), data["buy_price"], i + 1),
            }
            for i in range(data["rate_times"])
        ]
        return data

    def to_representation(self, instance):
        dict = super().to_representation(instance)
        return self.add_interests(data=dict)

    def to_internal_value(self, data):
        data = {
            "user": data["user"],
            "customer": {
                "id_person_number": data["birth_id"],
                "full_name": data["name"],
                "id_card_number": data["personal_id"],
                "id_card_number_expiration_date": data["personal_id_date"],
                "residence": data["address"],
                "nationality": data["nationality"],
                "place_of_birth": data["birth_place"],
                "sex": data["sex"],
            },
            "status": data["status"],
            "rate": data["interest_rate_or_amount"],
            "description": data["product_name"],
            "buy_price": data["product_buy"],
            "sell_price": utils.get_sell_price(
                rate=float(data["interest_rate_or_amount"]), buy_price=int(data["product_buy"])
            ),
            "date_extend": timezone.now(),
            "quantity": data["quantity"] if "quantity" in data else 1,
        }
        return super(ProductSerializer, self).to_internal_value(data)
