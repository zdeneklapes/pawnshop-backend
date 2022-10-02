from django.db import models


class StatisticOperation(models.TextChoices):
    # Loans
    LOAN_CREATE = "LOAN_CREATE", "Zastava"
    LOAN_EXTEND = "LOAN_EXTEND", "Prodlouzeni"
    LOAN_EXTEND_AFTER_MATURITY = "LOAN_EXTEND_AFTER_MATURITY", "Prodlouzeni po splatnosti"
    LOAN_RETURN = "LOAN_RETURN", "Vyber"
    # Offers
    OFFER_CREATE = "OFFER_CREATE", "Vykup"
    OFFER_SELL = "OFFER_SELL", "Prodej"
    # Move
    LOAN_TO_OFFER = "LOAN_TO_OFFER", "Presunuti do bazaru"
    # Logins
    LOGIN = "LOGIN", "Prihlaseni"
    LOGOUT = "LOGOUT", "Odhlaseni"
