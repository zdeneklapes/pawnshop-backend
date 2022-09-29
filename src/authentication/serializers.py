from django.contrib.auth import get_user_model
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from . import models

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = "__all__"


class AttendantProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    phone_number = PhoneNumberField(allow_null=False, allow_blank=False)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = models.AttendantProfile
        fields = "__all__"

    def validate(self, attrs):
        if self.Meta.model.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError(detail="User with email exists")

        if len(attrs["password"]) < 8:
            raise serializers.ValidationError(
                detail="User password must have at least 8 characters"
            )

        # TODO: Validate phone number

        return super().validate(attrs)

    def create(self, validated_data):
        user = self.Meta.model.objects.create(
            email=validated_data["email"],
            phone_number=validated_data["phone_number"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        if "password" in validated_data:
            user.set_password(validated_data["password"])
            user.save()
        return user


class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomerProfile
        fields = "__all__"
