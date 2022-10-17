from rest_framework import serializers

from authentication.models import User, AttendantProfile
from .base import UserBaseSerializer


class AttendantProfileSerializer(serializers.ModelSerializer, UserBaseSerializer):
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(min_length=8, write_only=True)
    old_or_verify_password = serializers.CharField(write_only=True)
    role = serializers.CharField(max_length=50, required=False)

    class Meta:
        model = AttendantProfile
        fields = ["id", "email", "password", "old_or_verify_password", "role"]

    def validate_create(self, attrs):
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError(detail="User with email exists")

        if attrs["password"] != attrs["old_or_verify_password"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        self.validate_new_password(attrs)

    def validate(self, attrs):
        if self.context["request"].stream.method == "POST":  # Create
            self.validate_create(attrs)

        if self.context["request"].stream.method == "PATCH":  # Update
            self.validate_update(attrs)

        return super().validate(attrs)

    def create(self, validated_data):
        user = AttendantProfile.objects.create_user(email=validated_data["email"], password=validated_data["password"])
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        if "password" in validated_data:
            user.set_password(validated_data["password"])
            user.save()
        return user
