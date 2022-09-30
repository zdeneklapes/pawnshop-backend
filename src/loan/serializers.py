from rest_framework import exceptions
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

    #
    # def update_helper_attendant(self, instance, validated_data):
    #     # Customer
    #     instance_customer, _ = CustomerProfile.objects.update_or_create(
    #         **validated_data["customer"]
    #     )
    #     instance.customer = instance_customer
    #     return instance
    #
    # def update_helper_admin(self, instance, validated_data):
    #     request_from_user = User.objects.get(email=self.context["request"].user)
    #     validated_data_product = validated_data["product"]
    #     instance_product = Product.objects.get(id=instance.product.id)
    #
    #     # Product
    #     if request_from_user.is_staff:
    #         instance_product.description = validated_data_product["description"]
    #         instance_product.save()
    #
    # def update_helper(self, instance, validated_data):
    #     self.update_helper_admin(instance, validated_data)
    #     return self.update_helper_attendant(instance, validated_data)
    #
    # def update(self, instance, validated_data):
    #     # Already payed loan
    #     if not instance.is_active:
    #         raise exceptions.PermissionDenied("Non active loans can't be updated")
    #
    #     # Customer is paying loan now
    #     if instance.is_active and "is_active" in validated_data and validated_data["is_active"] == False:
    #         instance.is_active = False
    #         Product.objects.get(id=instance.product).update_sell_price_based_on_week(
    #             rate=instance.rate
    #         )
    #
    #     # Else Update loan
    #     instance = self.update_helper(instance, validated_data)
    #     instance.save()
    #     return instance
