from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from authentication.serializers import CustomerProfileSerializer

from .models import models


class StatisticSerializer(WritableNestedModelSerializer):
    customer = CustomerProfileSerializer()
    sell_price = serializers.IntegerField(required=False)

    class Meta:
        model = models.Statistic
        fields = "__all__"
