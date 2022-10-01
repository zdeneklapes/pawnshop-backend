from datetime import datetime, date, timedelta
import typing
import copy

from rest_framework import mixins, permissions, response, viewsets, decorators, status, request
from rest_framework.settings import api_settings

from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from . import models, serializers
from product.models import Product


class CustomUpdateModelMixin:
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return response.Response(serializer.data)


class LoanViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    CustomUpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Loan.objects.before_maturity()
    serializer_class = serializers.LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def list(self, request, *args, **kwargs):
    #     queryset = models.Loan.before_maturity.before_maturity()
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     return response.Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance_product = Product.objects.get(id=instance.product.id)
        instance_product.update_sell_price_based_on_week(rate=instance.rate)
        instance.product = instance_product

        serializer = self.get_serializer(instance)
        return response.Response(serializer.data)


T = typing.TypeVar('T')


class RequestExtendDate(request.Request):
    @classmethod
    def new_data(cls, request: request.Request) -> request.Request:
        return {
            "product": {
                "id": request.data['product']['id'],
                "date_end": datetime.now()
            }
        }


class LoanPartialUpdateExtendDateViewSet(
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Loan.objects.all()
    serializer_class = serializers.LoanSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["patch"]

    def partial_update(self, request: request.Request, *args, **kwargs):
        request.data.update(RequestExtendDate.new_data(request))
        return super().partial_update(request, *args, **kwargs)


class LoanListAfterMaturityViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = models.Loan.objects.after_maturity()
    serializer_class = serializers.LoanSerializer
    permission_classes = [permissions.IsAuthenticated]
