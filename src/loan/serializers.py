from rest_framework import serializers

from . import models


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Loan
        fields = "__all__"
