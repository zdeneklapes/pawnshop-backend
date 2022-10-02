from rest_framework import serializers

from . import models


class CustomerProfileSerializer(serializers.ModelSerializer):
    id_birth = serializers.CharField(max_length=255)

    class Meta:
        model = models.CustomerProfile
        fields = "__all__"
