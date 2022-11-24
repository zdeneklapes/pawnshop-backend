# pylint: disable=E1101
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Group

from .choices import UserGroupChoice
from .managers import CustomUserManager


class User(AbstractUser):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    objects = CustomUserManager()

    base_role = UserGroupChoice.ADMIN
    role = models.CharField(max_length=50, choices=UserGroupChoice.choices)

    # Login via email & password (Switch these off)
    username = None
    first_name = None
    last_name = None

    # Auth field
    email = models.EmailField(max_length=255, unique=True)

    # Date
    date_joined = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    # Note: Must be here, otherwise produce error
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        self.role = self.base_role
        my_group = Group.objects.get(name=self.role)
        super().save(*args, **kwargs)
        self.refresh_from_db()
        if my_group:
            my_group.user_set.add(self)


class AttendantProfile(User):
    base_role = UserGroupChoice.ATTENDANT

    class Meta:
        verbose_name = "Attendant"
        verbose_name_plural = "Attendants"
        permissions = [
            ("base_role", "Can change role"),
            ("edit_custom_user", "Can edit custom user"),
            ("edit_cash_desk", "Can edit cash desk"),
            ("move_loan_to_offer", "Can move loan to offer"),
            ("sell_offer_without_eet", "Can sell offer without eet"),
            ("divide_product", "Can divide product"),
            ("edit_sell_price", "Can edit sell price"),
            ("edit_date", "Can edit date"),
            ("edit_subject", "Can edit subject"),
            ("edit_all_item", "Can edit all item"),
            ("see_price_in_stats", "Can see price in stats"),
            ("daily_stats", "Can see daily stats"),
            ("yield_stats", "Can see yield stats"),
            ("operate_on_shop", "Can operate on shop"),
            ("complete_win", "Can complete win"),
        ]
