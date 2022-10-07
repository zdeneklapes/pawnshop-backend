from django.db import models


class StatisticQPData(models.TextChoices):
    DEFAULT = "ALL", "Vsechny zaznamy"
    DAILY_STATS = "DAILY_STATS", "Denni statistiky"
    CASH_AMOUNT = "CASH_AMOUNT", "Stav pokladny"
    RESET = "RESET", "Reset profit"


class StatisticDescription(models.TextChoices):
    # Loans
    LOAN_CREATE = "LOAN_CREATE", "Zastava"
    LOAN_EXTEND = "LOAN_EXTEND", "Prodlouzeni"
    LOAN_EXTEND_AFTER_MATURITY = "LOAN_EXTEND_AFTER_MATURITY", "Prodlouzeni po splatnosti"
    LOAN_RETURN = "LOAN_RETURN", "Vyber"
    # Offers
    OFFER_BUY = "OFFER_BUY", "Vykup"
    OFFER_SELL = "OFFER_SELL", "Prodej"
    # Move
    LOAN_TO_OFFER = "LOAN_TO_OFFER", "Presunuti do bazaru"
    #
    UPDATE_DATA = "UPDATE_DATA", "Update data"
    # Logins
    LOGIN = "LOGIN", "Prihlaseni"
    LOGOUT = "LOGOUT", "Odhlaseni"
    #
    RESET = "RESET", "Reset profit"
