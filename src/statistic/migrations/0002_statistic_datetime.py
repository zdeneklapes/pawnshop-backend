# Generated by Django 4.1.1 on 2022-10-03 15:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("statistic", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="statistic",
            name="datetime",
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]