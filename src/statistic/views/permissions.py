from rest_framework import permissions
from rest_framework.request import Request

from statistic.models import StatisticQueryParams


class StatisticPermission(permissions.BasePermission):
    def has_permission(self, request: Request, view) -> bool:
        if request.method == "GET" and request.query_params.get("data") == StatisticQueryParams.ALL.name:
            return request.user.has_perm("statistic.view_statistic")
        if request.method == "GET" and request.query_params.get("data") == StatisticQueryParams.CASH_AMOUNT.name:
            return request.user.has_perm("statistic.data_cash_amount")
        if request.method == "GET" and request.query_params.get("data") == StatisticQueryParams.DAILY_STATS.name:
            return request.user.has_perm("statistic.data_daily_stats")
        if request.method == "POST" and request.data.get("update") == StatisticQueryParams.RESET.name:
            return request.user.has_perm("statistic.update_reset")

        return False
