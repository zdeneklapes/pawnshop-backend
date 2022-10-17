from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """Source: https://github.com/jod35/Pizza-delivery-API-Django"""

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Please enter an email address")

        email = self.normalize_email(email)
        new_user = self.model(email=email, **extra_fields)
        new_user.set_password(password)
        new_user.save()

        return new_user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        return self.create_user(email=email, password=password, **extra_fields)
