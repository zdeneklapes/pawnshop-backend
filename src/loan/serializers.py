from drf_writable_nested import WritableNestedModelSerializer

from authentication.serializers import CustomerProfileSerializer
from product.serializers import ProductSerializer

from . import models
from authentication.models import CustomerProfile, User
from product.models import Product


class LoanSerializer(WritableNestedModelSerializer):
    product = ProductSerializer()
    customer = CustomerProfileSerializer()

    class Meta:
        model = models.Loan
        fields = ["user", "shop", "rate", "is_active", "product", "customer"]

    def update(self, instance, validated_data):
        # User which created request
        request_user = User.objects.get(email=self.context["request"].user)

        # Customer
        instance_customer, _ = CustomerProfile.objects.update_or_create(
            id_person_number=instance.customer.id_person_number
        )
        instance.customer = instance_customer

        # Product
        validated_data_product = validated_data["product"]
        instance_product = Product.objects.get(id=instance.product.id)
        instance_product.is_active = validated_data_product["is_active"]

        if request_user.is_staff:
            instance_product.description = validated_data_product["description"]

        instance_product.save()

        # Loan
        instance.shop = validated_data["shop"]
        instance.rate = validated_data["rate"]
        instance.save()

        return instance
