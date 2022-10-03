# Generated by Django 4.1.1 on 2022-10-03 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("statistic", "0002_statistic_datetime"),
    ]

    operations = [
        migrations.AlterField(
            model_name="statistic",
            name="description",
            field=models.CharField(
                choices=[
                    ("LOAN_CREATE", "Zastava"),
                    ("LOAN_EXTEND", "Prodlouzeni"),
                    ("LOAN_EXTEND_AFTER_MATURITY", "Prodlouzeni po splatnosti"),
                    ("LOAN_RETURN", "Vyber"),
                    ("OFFER_CREATE", "Vykup"),
                    ("OFFER_SELL", "Prodej"),
                    ("LOAN_TO_OFFER", "Presunuti do bazaru"),
                    ("LOGIN", "Prihlaseni"),
                    ("LOGOUT", "Odhlaseni"),
                    ("RESET", "Reset profit"),
                ],
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="statistic",
            name="price",
            field=models.IntegerField(default=0),
        ),
    ]