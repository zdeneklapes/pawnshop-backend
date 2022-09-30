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

    def update(self, instance, validated_data):
        pass
        # instance.nr = validated_data.get('', instance.nr)
        # instance.title = validated_data.get('title', instance.title)
        # instance.save()
        #
        # items = validated_data.get('items')
        #
        # for item in items:
        #     item_id = item.get('id', None)
        #     if item_id:
        #         inv_item = InvoiceItem.objects.get(id=item_id, invoice=instance)
        #         inv_item.name = item.get('name', inv_item.name)
        #         inv_item.price = item.get('price', inv_item.price)
        #         inv_item.save()
        #     else:
        #         InvoiceItem.objects.create(account=instance, **item)
        #
        # return instance

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
