# Generated by Django 4.1.3 on 2022-11-28 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CustomerProfile",
            fields=[
                ("id_birth", models.CharField(max_length=255, primary_key=True, serialize=False)),
                ("full_name", models.CharField(max_length=255)),
                ("personal_id", models.CharField(max_length=255)),
                ("personal_id_expiration_date", models.DateField()),
                ("residence", models.CharField(max_length=255)),
                ("nationality", models.CharField(max_length=255)),
                ("birthplace", models.CharField(max_length=255)),
                ("sex", models.CharField(choices=[("M", "Male"), ("F", "Female")], max_length=1)),
            ],
        ),
    ]
