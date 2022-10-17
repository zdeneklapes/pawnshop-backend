from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from . import models
from config.settings import AUTH


# User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(min_length=8, write_only=True)
    role = serializers.CharField(max_length=50, required=False)

    class Meta:
        model = models.User
        fields = ["id", "email", "password", "role"]


# class ChangePasswordSerializer(serializers.ModelSerializer):
#     """Source: https://medium.com/django-rest/django-rest-framework-change-password-and-update-profile-1db0c144c0a"""
#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)
#     old_password = serializers.CharField(write_only=True, required=True)
#
#     class Meta:
#         model = models.User
#         fields = ('old_password', 'password', 'password2')
#
#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({"password": "Password fields didn't match."})
#
#         return attrs
#
#     def validate_password(self):
#         pass
#
#     def validate_old_password(self, value):
#         user = self.context['request'].user
#         if not user.check_password(value):
#             raise serializers.ValidationError({"old_password": "Old password is not correct"})
#         return value
#
#     def update(self, instance, validated_data):
#
#         instance.set_password(validated_data['password'])
#         instance.save()
#
#         return instance


class AttendantProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(min_length=8, write_only=True)
    password2 = serializers.CharField(min_length=8, write_only=True)
    role = serializers.CharField(max_length=50, required=False)

    class Meta:
        model = models.AttendantProfile
        fields = ["id", "email", "password", "password2", "role"]

    def validate(self, attrs):
        attrs_new = {}

        # TODO:
        # if self.Meta.model.objects.filter(email=attrs["email"]).exists():
        #     raise serializers.ValidationError(detail="User with email exists")

        if AUTH and self.context["request"].user.role != "ADMIN":
            attrs_new["email"] = attrs["email"]
            attrs_new["password"] = attrs["password"]
            return super().validate(attrs_new)

        if len(attrs["password"]) < 8:
            raise serializers.ValidationError(detail="User password must have at least 8 characters")

        return super().validate(attrs)

    def create(self, validated_data):
        user = models.AttendantProfile.objects.create_user(
            email=validated_data["email"], password=validated_data["password"]
        )
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        # TODO: Not workign password update
        if "password" in validated_data:
            # models.User.objects.update(id=user.id, password=validated_data["password"])
            # user.update(password=validated_data["password"])
            user.set_password(validated_data["password"])
            user.save()
        return user


# class RegisterSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(
#         required=True,
#         validators=[UniqueValidator(queryset=models.User.objects.all())]
#     )
#
#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)
#
#     class Meta:
#         model = models.User
#         fields = ('password', 'password2', 'email')
#
#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({"password": "Password fields didn't match."})
#
#         return attrs
#
#     def create(self, validated_data):
#         user = models.User.objects.create(
#             email=validated_data['email'],
#         )
#
#         user.set_password(validated_data['password'])
#         user.save()
#
#         return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["role"] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        return data
