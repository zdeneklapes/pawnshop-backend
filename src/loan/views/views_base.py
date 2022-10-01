from rest_framework import mixins, permissions, response, viewsets

from loan import models, serializers
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
