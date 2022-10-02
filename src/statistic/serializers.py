from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer


from .models import models


class StatisticSerializer(WritableNestedModelSerializer):
    amount = serializers.IntegerField(required=False)

    class Meta:
        model = models.Statistic
        fields = "__all__"

    @classmethod
    def save_statistics(self, price: int, operation: str, user: int, product: int = None):
        serializer_stats = StatisticSerializer(
            data={"description": operation, "price": price, "product": product, "user": user}
        )
        serializer_stats.is_valid()
        serializer_stats.save()
