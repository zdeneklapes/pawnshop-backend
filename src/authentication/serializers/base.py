from rest_framework import serializers

from authentication.models import UserRoleChoice


class UserBaseSerializer(serializers.Serializer):
    def validate_new_password(self, attrs):
        if len(attrs["password"]) < 8:
            raise serializers.ValidationError(detail="User password must have at least 8 characters")

    def validate_old_password(self, value):
        # if not self.context["request"].user.check_password(value):
        if not self.instance.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def validate_update(self, attrs):
        var_search_1 = "old_or_verify_password"

        self.validate_new_password(attrs)

        if var_search_1 not in attrs:
            raise serializers.ValidationError({"old_or_verify_password": "This field must be provided"})

        self.validate_old_password(attrs[var_search_1])

        if (
            self.context["request"].user.role != UserRoleChoice.ADMIN.name
            and self.context["request"].user.id != self.instance.id
        ):
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})
