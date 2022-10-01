from datetime import datetime
import typing

from rest_framework import mixins, permissions, request, response, viewsets


from . import models, serializers
from product.models import Product


class CustomUpdateModelMixin:
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return response.Response(serializer.data)


class LoanListAfterMaturityViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    # queryset = models.Loan.objects.after_maturity()
    # serializer_class = serializers.LoanSerializer
    # permission_classes = [permissions.IsAuthenticated]
    # TODO: This Route not working
    queryset = models.Loan.objects.after_maturity()
    serializer_class = serializers.LoanSerializer
    permission_classes = [permissions.IsAuthenticated]


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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance_product = Product.objects.get(id=instance.product.id)
        instance_product.update_sell_price_based_on_week(rate=instance.rate)
        instance.product = instance_product

        serializer = self.get_serializer(instance)
        return response.Response(serializer.data)


T = typing.TypeVar("T")


class RequestExtendDate(request.Request):
    @classmethod
    def new_data(cls, request: request.Request) -> request.Request:
        return {
            "product": {"id": request.data["product"]["id"], "date_end": datetime.now()}
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
