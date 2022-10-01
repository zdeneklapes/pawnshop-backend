from rest_framework import exceptions
from drf_writable_nested import WritableNestedModelSerializer

from authentication.serializers import CustomerProfileSerializer, UserSerializer
from shop.serializers import ShopSerializer

from . import models


class LoanSerializer(WritableNestedModelSerializer):
    user = UserSerializer()
    customer = CustomerProfileSerializer()
    shop = ShopSerializer()

    class Meta:
        model = models.Product
        fields = "__all__"

class AfterMaturitySerialzier(WritableNestedModelSerializer):
    pass

class OfferSerializer(WritableNestedModelSerializer):
    pass
