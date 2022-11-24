# Generated by Django 4.1.3 on 2022-11-24 15:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
                (
                    "role",
                    models.CharField(
                        choices=[("ADMIN_ADMIN", "Root Admin"), ("ADMIN", "Admin"), ("ATTENDANT", "Attendant")],
                        max_length=50,
                    ),
                ),
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
                "verbose_name": "User",
                "verbose_name_plural": "Users",
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
            ],
            options={
                "verbose_name": "Attendant",
                "verbose_name_plural": "Attendants",
                "permissions": [
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
                ],
            },
            bases=("authentication.user",),
        ),
    ]
