from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from authentication.models import CustomerProfile
from authentication.serializers import CustomerProfileSerializer
from product.serializers import ProductSerializer

from . import models


class LoanSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    customer = CustomerProfileSerializer()

    class Meta:
        model = models.Loan
        fields = ["user", "shop", "rate", "is_active", "product", "customer"]

    def create(self, validated_data):
        # Product
        product_serializer = ProductSerializer(data=validated_data.pop("product"))
        product_serializer.is_valid(raise_exception=True)
        validated_data["product"] = product_serializer.save()

        # Customer
        customer = validated_data.pop("customer")
        try:
            customer = CustomerProfile.objects.get(
                id_person_number=customer.get("id_person_number")
            )
        except (ObjectDoesNotExist, AttributeError):
            customer_serializer = CustomerProfileSerializer(data=customer)
            customer_serializer.is_valid(raise_exception=True)
            customer = customer_serializer.save()
        else:
            validated_data["customer"] = customer

        # return super(LoanSerializer, self).create(validated_data)
        return self.Meta.model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass
