# pylint: disable=E1101
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Group

from shop.models import Shop
from .choices import UserRoleChoice
from .managers import CustomUserManager


class User(AbstractUser):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    objects = CustomUserManager()

    base_role = UserRoleChoice.ADMIN
    role = models.CharField(max_length=50, choices=UserRoleChoice.choices)

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
            my_group.user_set.remove(self)


class AttendantProfile(User):
    class Meta:
        verbose_name = "Attendant"
        verbose_name_plural = "Attendants"

    base_role = UserRoleChoice.ATTENDANT

    # Customer
    perm_edit_custom_user = models.BooleanField(default=False)

    # Cash desk
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
