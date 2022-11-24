# Generated by Django 4.1.3 on 2022-11-24 11:40

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Shop",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("address", models.CharField(max_length=255, unique=True)),
                ("town", models.CharField(max_length=255)),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(max_length=20, region=None, unique=True),
                ),
                ("open_hours", models.TimeField()),
                ("close_hours", models.TimeField()),
                ("is_active", models.BooleanField(default=True)),
            ],
        ),
    ]
