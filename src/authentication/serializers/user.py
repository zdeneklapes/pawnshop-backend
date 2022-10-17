from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from authentication.models import User, AttendantProfile
from authentication.models import UserRoleChoice


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(min_length=8, write_only=True)
    role = serializers.CharField(max_length=50, required=False)

    class Meta:
        model = User
        fields = ["id", "email", "password", "role"]


class AttendantProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(min_length=8, write_only=True)
    old_or_verify_password = serializers.CharField(min_length=8, write_only=True)
    role = serializers.CharField(max_length=50, required=False)

    class Meta:
        model = AttendantProfile
        fields = ["id", "email", "password", "old_or_verify_password", "role"]

    def validate_new_password(self, attrs):
        if len(attrs["password"]) < 8:
            raise serializers.ValidationError(detail="User password must have at least 8 characters")

    def validate_create(self, attrs):
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError(detail="User with email exists")

        if attrs["password"] != attrs["old_or_verify_password"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        self.validate_new_password(attrs)

    def validate_old_password(self, value):
        user = self.context["request"].admin

        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def validate_update(self, attrs):
        var_search_1 = "old_or_verify_password"

        self.validate_new_password(attrs)

        if var_search_1 not in attrs:
            raise serializers.ValidationError({"old_or_verify_password": "This field must be provided"})

        self.validate_old_password(attrs[var_search_1])

        if (
            self.context["request"].admin.role != UserRoleChoice.ADMIN.name
            and self.context["request"].admin.id != self.instance.id
        ):
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

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


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["role"] = user.role
        return token
