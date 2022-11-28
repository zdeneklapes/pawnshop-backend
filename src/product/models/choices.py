from django.db import models


class RateFrequency(models.TextChoices):
    DAY = "DAY", "Day"
    WEEK = "WEEK", "Week"
    YEAR = "YEAR", "Year"


class ProductStatusOrData(models.TextChoices):
    # Status
    OFFER = "OFFER", "Bazar"
    LOAN = "LOAN", "Zastavarna"
    AFTER_MATURITY = "AFTER_MATURITY", "Mezisklad"
    INACTIVE_LOAN = "INACTIVE_LOAN", "Neaktivní zastava"
    INACTIVE_OFFER = "INACTIVE_OFFER", "Neaktivní bazar"


class ProductShopData(models.TextChoices):
    # Statistics Data
    SHOP_STATS = "SHOP_STATS", "Statistiky obchodu"
