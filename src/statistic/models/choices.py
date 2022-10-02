from django.db import models
from rest_framework.request import Request
from typing import Tuple

from common.exceptions import BadQueryParam


class StatisticOperations(models.TextChoices):
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

    @staticmethod
    def validate_operation(request: Request, buy_price_prev: int, sell_price_prev: int) -> Tuple[str, int]:
        if "operation" not in request.query_params:
            raise BadQueryParam()
        else:
            operation = request.query_params["operation"]
            if operation == StatisticOperations.LOAN_EXTEND.name:  # pylint: disable=E1101
                price = sell_price_prev - buy_price_prev
            elif operation == StatisticOperations.LOAN_RETURN.name:  # pylint: disable=E1101
                price = sell_price_prev
            elif operation == StatisticOperations.LOAN_TO_OFFER.name:  # pylint: disable=E1101
                price = 0
            else:
                raise BadQueryParam()
        return operation, price
