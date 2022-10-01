from django.db import models


class StatisticOperation(models.TextChoices):
    # Loans
    CREATE_LOAN = "ZASTAVA", "Zastava"
    EXTEND_DATE = "PRODLOUZENI", "Prodlouzeni"
    RETURN_LOAN = "VYBER", "Vyber"
    # Offers
    CREATE_OFFER = "ZASTAVA", "Zastava"
    SELL_OFFER = "ZASTAVA", "Zastava"
    # Logins
    LOGIN = "PRIHLASENI", "Prihlaseni"
    LOGOUT = "ODHLASENI", "Odhlaseni"
