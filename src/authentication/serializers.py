from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    snippet = serializers.PrimaryKeyRelatedField(
        many=True, queryset=models.User.objects.all()
    )

    class Meta:
        model = models.User
        fields = [""]  # TODO
