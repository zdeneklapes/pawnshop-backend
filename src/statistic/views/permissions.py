from rest_framework import permissions
from rest_framework.request import Request

from statistic.models import StatisticQueryParams


class StatisticPermission(permissions.BasePermission):
    def has_permission(self, request: Request, view) -> bool:
        model = "statistic"
        if request.method == "GET" and request.query_params.get("data") == StatisticQueryParams.ALL.name:
            return request.user.has_perm(f"{model}.view_statistic")
        if request.method == "GET" and request.query_params.get("data") == StatisticQueryParams.CASH_AMOUNT.name:
            return request.user.has_perm(f"{model}.view_cash_amount")
        if request.method == "GET" and request.query_params.get("data") == StatisticQueryParams.DAILY_STATS.name:
            return request.user.has_perm(f"{model}.view_daily_stats")
        if request.method == "POST" and request.data.get("update") == StatisticQueryParams.RESET.name:
            return request.user.has_perm(f"{model}.reset_profit")

        return False
