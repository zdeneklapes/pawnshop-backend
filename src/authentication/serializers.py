from rest_framework import serializers

from . import models


class AttendantProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttendantProfile
        fields = "__all__"
