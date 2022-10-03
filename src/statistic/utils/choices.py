from django.db import models


class StatisticQueryParamsChoices(models.TextChoices):
    DEFAULT = "ALL", "Vsechny zaznamy"
    DAILY_STATS = "DAILY_STATS", "Denni statistiky"
    CASH_AMOUNT = "CASH_AMOUNT", "Stav pokladny"
    SHOP_STATE = "SHOP_STATE", "Stav obchodu"
    RESET = "RESET", "Reset profit"
