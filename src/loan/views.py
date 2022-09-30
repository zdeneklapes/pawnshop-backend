from datetime import datetime, date, timedelta
import typing

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
    queryset = models.Loan.objects.all()
    serializer_class = serializers.LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = models.Loan.before_maturity.before_maturity()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance_product = Product.objects.get(id=instance.product.id)
        instance_product.update_sell_price_based_on_week(rate=instance.rate)
        instance.product = instance_product

        serializer = self.get_serializer(instance)
        return response.Response(serializer.data)


T = typing.TypeVar('T')

class QueryParams(typing.Generic[T]):
    pk: T


class ExtendDateInterface(QueryParams[T]):
    pass


class LoanExtendDateViewSet(
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Loan.objects.all()
    serializer_class = serializers.LoanSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["patch"]

    def partial_update(self, request: request.Request, *args, **kwargs):
        # serializer_ ExtendDateInterface()
        
        instance = self.get_object()
        instance_product = Product.objects.get(id=instance.product.id)
        instance_product.date_extended_deadline = datetime.now()
        instance_product.date_end = date.today() + timedelta(weeks=4)
        instance_product.update_sell_price_based_on_week(rate=instance.rate)
        instance.product = instance_product

        # Serialize
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid()
        serializer.save()
        return response.Response(serializer.data)


class LoanAfterMaturityViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.Loan.objects.all()  # after_maturity.after_maturity()
    serializer_class = serializers.LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = (
            models.Loan.after_maturity.after_maturity()
        )  # self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)
