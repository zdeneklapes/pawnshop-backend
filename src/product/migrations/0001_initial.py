# Generated by Django 4.1.2 on 2022-10-17 20:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("customer", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("OFFER", "Offer"),
                            ("LOAN", "Loan"),
                            ("AFTER_MATURITY", "After_maturity"),
                            ("INACTIVE_LOAN", "Inactive_loan"),
                            ("INACTIVE_OFFER", "Inactive_offer"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "rate_frequency",
                    models.CharField(
                        choices=[("DAY", "Day"), ("WEEK", "Week"), ("YEAR", "Year")], default="WEEK", max_length=50
                    ),
                ),
                ("rate_times", models.PositiveIntegerField(default=4)),
                ("interest_rate_or_quantity", models.DecimalField(decimal_places=1, max_digits=4, null=True)),
                ("product_name", models.TextField()),
                ("buy_price", models.PositiveIntegerField()),
                ("sell_price", models.PositiveIntegerField(null=True)),
                ("inventory_id", models.PositiveIntegerField()),
                ("date_create", models.DateTimeField(null=True)),
                ("date_extend", models.DateTimeField(null=True)),
                ("date_end", models.DateTimeField(null=True)),
                (
                    "customer",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="customer.customerprofile"),
                ),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
