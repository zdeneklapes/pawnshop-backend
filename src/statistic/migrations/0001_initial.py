# Generated by Django 4.1.3 on 2022-11-24 12:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("product", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Statistic",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("datetime", models.DateTimeField(auto_now_add=True)),
                (
                    "description",
                    models.CharField(
                        choices=[
                            ("LOAN_CREATE", "Zastava"),
                            ("LOAN_EXTEND", "Prodlouzeni"),
                            ("LOAN_EXTEND_AFTER_MATURITY", "Prodlouzeni po splatnosti"),
                            ("LOAN_RETURN", "Vyber"),
                            ("OFFER_BUY", "Vykup"),
                            ("OFFER_SELL", "Prodej"),
                            ("LOAN_TO_OFFER", "Presunuti do bazaru"),
                            ("UPDATE_DATA", "Produkt aktualizovan"),
                            ("LOGIN", "Prihlaseni"),
                            ("LOGOUT", "Odhlaseni"),
                            ("RESET", "Reset profit"),
                        ],
                        max_length=255,
                    ),
                ),
                ("price", models.IntegerField(default=0)),
                ("amount", models.IntegerField()),
                ("profit", models.IntegerField()),
                (
                    "product",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to="product.product"),
                ),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "permissions": (
                    ("view_cash_amount", "Can view cash amount"),
                    ("view_daily_stats", "Can view daily stats"),
                    ("reset_profit", "Can reset profit"),
                ),
            },
        ),
    ]
