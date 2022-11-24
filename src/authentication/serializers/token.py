from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework import serializers

from statistic.models.choices import StatisticDescription
from statistic.serializers.statistic import StatisticSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["role"] = user.role
        StatisticSerializer.save_statistic_auth(StatisticDescription.LOGIN.name, user.id)
        return token


class LogoutAllSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    # def validate(self, attrs):
    #     self.token = attrs["refresh"]
    #     return attrs

    def save(self, **kwargs):
        try:
            # RefreshToken(self.token).blacklist()
            StatisticSerializer.save_statistic_auth(StatisticDescription.LOGOUT.name, self.context["request"].user.id)
        except TokenError as e:
            raise serializers.ValidationError({"bad_token": ("Token is invalid or expired")}) from e
