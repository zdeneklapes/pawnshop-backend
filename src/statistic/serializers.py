from drf_writable_nested import WritableNestedModelSerializer


from .models import models


class StatisticSerializer(WritableNestedModelSerializer):
    class Meta:
        model = models.Statistic
        fields = "__all__"
