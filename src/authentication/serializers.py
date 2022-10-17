from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from . import models

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(min_length=8, write_only=True)
    role = serializers.CharField(max_length=50, required=False)

    class Meta:
        model = models.User
        fields = ["id", "email", "password", "role"]


class AttendantProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(min_length=8, write_only=True)
    role = serializers.CharField(max_length=50, required=False)

    class Meta:
        model = models.AttendantProfile
        fields = ["id", "email", "password", "role"]

    def validate(self, attrs):
        attrs_new = {}

        # TODO:
        # if self.Meta.model.objects.filter(email=attrs["email"]).exists():
        #     raise serializers.ValidationError(detail="User with email exists")

        if self.context["request"].user.role != "ADMIN":
            attrs_new["email"] = attrs["email"]
            attrs_new["password"] = attrs["password"]
            return super().validate(attrs_new)

        if len(attrs["password"]) < 8:
            raise serializers.ValidationError(detail="User password must have at least 8 characters")

        return super().validate(attrs)

    def create(self, validated_data):
        user = self.Meta.model.objects.create(
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        # TODO: Not workign password update
        if "password" in validated_data:
            user.set_password(validated_data["password"])
            user.save()
        return user


class TokenUser:
    @staticmethod
    def add_user_to_data(data, user):
        data["user"] = {"id": user.id, "email": user.email, "role": user.role}
        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["role"] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data = TokenUser.add_user_to_data(data, self.user)
        return data
