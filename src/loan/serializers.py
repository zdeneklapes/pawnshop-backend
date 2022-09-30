from drf_writable_nested import WritableNestedModelSerializer

from authentication.serializers import CustomerProfileSerializer
from product.serializers import ProductSerializer

from . import models


class LoanSerializer(WritableNestedModelSerializer):
    product = ProductSerializer()
    customer = CustomerProfileSerializer()

    class Meta:
        model = models.Loan
        fields = ["user", "shop", "rate", "is_active", "product", "customer"]

    # def create(self, validated_data):
    #     """Source: https://stackoverflow.com/a/31008488/14471542"""
    #     # Product
    #     product_serializer = ProductSerializer(data=validated_data.pop("product"))
    #     product_serializer.is_valid(raise_exception=True)
    #     validated_data["product"] = product_serializer.save()
    #
    #     # Customer
    #     customer = validated_data.pop("customer")
    #     try:
    #         customer = CustomerProfile.objects.get(
    #             id_person_number=customer.get("id_person_number")
    #         )
    #     except (ObjectDoesNotExist, AttributeError):
    #         customer_serializer = CustomerProfileSerializer(data=customer)
    #         customer_serializer.is_valid(raise_exception=True)
    #         customer = customer_serializer.save()
    #     else:
    #         validated_data["customer"] = customer
    #
    #     return super(LoanSerializer, self).create(validated_data)
    #
    # def update(self, instance, validated_data):
    #     pass
