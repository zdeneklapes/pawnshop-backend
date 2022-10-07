from django.db import models
from rest_framework.request import Request
from typing import Tuple

from common.exceptions import BadQueryParam


class StatisticQPData(models.TextChoices):
    DEFAULT = "ALL", "Vsechny zaznamy"
    DAILY_STATS = "DAILY_STATS", "Denni statistiky"
    CASH_AMOUNT = "CASH_AMOUNT", "Stav pokladny"
    SHOP_STATS = "SHOP_STATS", "Stav obchodu"
    RESET = "RESET", "Reset profit"


class StatisticDescription(models.TextChoices):
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
    #
    UPDATE = "UPDATE", "Update"
    # Logins
    LOGIN = "LOGIN", "Prihlaseni"
    LOGOUT = "LOGOUT", "Odhlaseni"
    #
    RESET = "RESET", "Reset profit"

    @staticmethod
    def validate_operation(request: Request, buy_price_prev: int, sell_price_prev: int) -> Tuple[str, int]:
        if "operation" not in request.query_params:
            raise BadQueryParam()
        else:
            operation = request.query_params["operation"]
            if operation == StatisticDescription.LOAN_EXTEND.name:  # pylint: disable=E1101
                price = sell_price_prev - buy_price_prev
            elif operation == StatisticDescription.LOAN_RETURN.name:  # pylint: disable=E1101
                price = sell_price_prev
            elif operation == StatisticDescription.LOAN_TO_OFFER.name:  # pylint: disable=E1101
                price = 0
            elif operation == StatisticDescription.OFFER_SELL.name:  # pylint: disable=E1101
                price = sell_price_prev
            elif operation == StatisticDescription.OFFER_SELL.name:  # pylint: disable=E1101
                price = sell_price_prev
            elif operation == StatisticDescription.UPDATE.name:  # pylint: disable=E1101
                price = 0
            else:
                raise BadQueryParam()
        return operation, price
