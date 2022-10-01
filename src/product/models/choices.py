from django.db import models


class RateFrequency(models.TextChoices):
    DAY = "DAY", "Day"
    WEEK = "WEEK", "Week"
    YEAR = "YEAR", "Year"


class ProductStatus(models.TextChoices):
    OFFER = "OFFER", "Offer"
    LOAN = "LOAN", "Loan"
    AFTER_MATURITY = "AFTER_MATURITY", "After_maturity"
    INACTIVE_LOAN = "INACTIVE_LOAN", "Inactive_loan"
    INACTIVE_OFFER = "INACTIVE_OFFER", "Inactive_offer"
