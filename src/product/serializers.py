from rest_framework import exceptions, serializers
from drf_writable_nested import WritableNestedModelSerializer

from authentication.serializers import CustomerProfileSerializer, UserSerializer
from shop.serializers import ShopSerializer

from . import models
from authentication.models import User


class ProductSerializer(WritableNestedModelSerializer):
    customer = CustomerProfileSerializer()
    sell_price = serializers.IntegerField(required=False)

    class Meta:
        model = models.Product
        fields = "__all__"
        # fields = ["user", "rate", "is_active", "product", "customer"]


class AfterMaturitySerialzier(WritableNestedModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"


class OfferSerializer(WritableNestedModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"
