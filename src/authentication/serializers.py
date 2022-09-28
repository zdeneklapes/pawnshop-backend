from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = "__all__"


class AttendantProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttendantProfile
        fields = "__all__"


class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomerProfile
        fields = "__all__"
