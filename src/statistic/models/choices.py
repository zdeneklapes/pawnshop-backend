from django.db import models


class StatisticQueryParams(models.TextChoices):
    ALL = "ALL", "Vsechny zaznamy"
    DAILY_STATS = "DAILY_STATS", "Denni statistiky"
    CASH_AMOUNT = "CASH_AMOUNT", "Stav pokladny"
    RESET = "RESET", "Reset profit"


class StatisticDescription(models.TextChoices):
    # Loans
    LOAN_CREATE = "LOAN_CREATE", "Zástava"
    LOAN_EXTEND = "LOAN_EXTEND", "Prodloužení"
    LOAN_EXTEND_AFTER_MATURITY = "LOAN_EXTEND_AFTER_MATURITY", "Prodloužení po splatnosti"
    LOAN_RETURN = "LOAN_RETURN", "Výběr"
    # Offers
    OFFER_BUY = "OFFER_BUY", "Výkup"
    OFFER_SELL = "OFFER_SELL", "Prodej"
    # Move
    LOAN_TO_OFFER = "LOAN_TO_OFFER", "Přesunutí do bazaru"
    #
    UPDATE_DATA = "UPDATE_DATA", "Produkt aktualizován"
    # Logins
    LOGIN = "LOGIN", "Přihlášení"
    LOGOUT = "LOGOUT", "Odhlášení"
    #
    RESET = "RESET", "Profit nulován"
