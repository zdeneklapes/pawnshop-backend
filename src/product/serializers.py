from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from authentication.serializers import CustomerProfileSerializer

from . import models


class ProductSerializer(WritableNestedModelSerializer):
    customer = CustomerProfileSerializer()
    sell_price = serializers.IntegerField(required=False)

    class Meta:
        model = models.Product
        fields = "__all__"
        # fields = ["user", "rate", "is_active", "product", "customer"]
