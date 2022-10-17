from rest_framework import serializers

from authentication.models import UserRoleChoice, User
from config.settings import AUTH


class UserBaseSerializer(serializers.Serializer):
    def validate_new_password(self, attrs):
        if len(attrs["password"]) < 8:
            raise serializers.ValidationError(detail="User password must have at least 8 characters")

        if attrs["password"] != attrs["verify_password"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

    def validate_old_password(self, value):
        if not self.instance.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def validate_update(self, attrs):
        var_search_1 = "old_password"
        var_search_2 = "verify_password"

        self.validate_new_password(attrs)

        if var_search_1 not in attrs or var_search_2 not in attrs:
            raise serializers.ValidationError(
                {var_search_1: "This field must be provided", var_search_2: "This field must be provided"}
            )

        self.validate_old_password(attrs[var_search_1])

        if (
            AUTH
            and self.context["request"].user.role != UserRoleChoice.ADMIN.name
            and self.context["request"].user.id != self.instance.id
        ):
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

    def validate_create(self, attrs):
        var_search_2 = "verify_password"

        if var_search_2 not in attrs:
            raise serializers.ValidationError({var_search_2: "This field must be provided"})

        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError(detail="User with email exists")

        if attrs["password"] != attrs["verify_password"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        self.validate_new_password(attrs)

    def validate(self, attrs):
        if self.context["request"].stream.method == "POST":  # Create
            self.validate_create(attrs)

        if self.context["request"].stream.method == "PATCH":  # Update
            self.validate_update(attrs)

        return super().validate(attrs)
