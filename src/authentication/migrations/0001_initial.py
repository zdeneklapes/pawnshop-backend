# Generated by Django 4.1.2 on 2022-10-22 13:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("shop", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                ("role", models.CharField(choices=[("ADMIN", "Admin"), ("ATTENDANT", "Attendant")], max_length=50)),
                ("email", models.EmailField(max_length=255, unique=True)),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
                ("date_update", models.DateTimeField(auto_now=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="AttendantProfile",
            fields=[
                (
                    "user_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("perm_edit_custom_user", models.BooleanField(default=False)),
                ("perm_edit_cash_desk", models.BooleanField(default=False)),
                ("perm_move_loan_to_offer", models.BooleanField(default=False)),
                ("perm_sell_offer_without_eet", models.BooleanField(default=False)),
                ("perm_divide_product", models.BooleanField(default=False)),
                ("perm_edit_sell_price", models.BooleanField(default=False)),
                ("perm_edit_date", models.BooleanField(default=False)),
                ("perm_edit_subject", models.BooleanField(default=False)),
                ("perm_edit_all_item", models.BooleanField(default=False)),
                ("perm_see_price_in_stats", models.BooleanField(default=False)),
                ("perm_daily_stats", models.BooleanField(default=False)),
                ("perm_yield_stats", models.BooleanField(default=False)),
                ("perm_complete_win", models.BooleanField(default=False)),
                ("perm_operate_on_shop", models.ManyToManyField(blank=True, to="shop.shop")),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            bases=("authentication.user",),
        ),
    ]
