from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from shop.models import Shop


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


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        ATTENDANT = "ATTENDANT", "Attendant"

    objects = CustomUserManager()

    base_role = Role.ADMIN
    role = models.CharField(max_length=50, choices=Role.choices)

    # Login via email & password (Switch these off)
    username = None
    first_name = None
    last_name = None

    # Auth field
    email = models.EmailField(max_length=255, unique=True)
    phone_number = PhoneNumberField(max_length=20, unique=True)

    # Date
    date_joined = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    # Note: Must be here, otherwise produce error
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)


class AttendantProfile(User):
    base_role = User.Role.ATTENDANT

    # Customer
    perm_edit_custom_user = models.BooleanField(default=False)

    # Cashdesk
    perm_edit_cash_desk = models.BooleanField(default=False)

    # Loan
    perm_move_loan_to_offer = models.BooleanField(default=False)
    perm_sell_offer_without_eet = models.BooleanField(default=False)
    perm_divide_product = models.BooleanField(default=False)  # TODO: Later

    # Product
    perm_edit_sell_price = models.BooleanField(default=False)
    perm_edit_date = models.BooleanField(default=False)
    perm_edit_subject = models.BooleanField(default=False)
    perm_edit_all_item = models.BooleanField(default=False)  # TODO: For what?

    # Statistic
    perm_see_price_in_stats = models.BooleanField(default=False)
    perm_daily_stats = models.BooleanField(default=False)
    perm_yield_stats = models.BooleanField(default=False)

    # Shop
    perm_operate_on_shop = models.ManyToManyField(Shop, blank=True)

    # Others
    perm_complete_win = models.BooleanField(default=False)  # TODO: For what?


class CustomerProfile(models.Model):
    GENDERS_CHOICES = (("M", "Male"), ("F", "Female"))

    id_person_number = models.CharField(primary_key=True, max_length=255)
    full_name = models.CharField(max_length=255)
    id_card_number = models.CharField(max_length=255)
    id_card_number_expiration_date = models.DateField()
    residence = models.CharField(max_length=255)
    citizenship = models.CharField(max_length=255)
    place_of_birth = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDERS_CHOICES)


class UserLoginActivity(models.Model):
    """TODO"""

    LOGIN_STATUS = (("S", "Success"), ("F", "Failed"))

    login_IP = models.GenericIPAddressField(null=True, blank=True)
    login_datetime = models.DateTimeField(auto_now=True)
    login_username = models.CharField(max_length=40, null=True, blank=True)
    status = models.CharField(
        max_length=1, default="S", choices=LOGIN_STATUS, null=True, blank=True
    )
    user_agent_info = models.CharField(max_length=255)

    class Meta:
        verbose_name = "user_login_activity"
        verbose_name_plural = "user_login_activities"
