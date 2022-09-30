from rest_framework import mixins, permissions, response, viewsets, decorators

from . import models, serializers
from product.models import Product


class LoanViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Loan.objects.all()
    serializer_class = serializers.LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = (
            models.Loan.before_maturity.before_maturity()
        )  # self.filter_queryset(self.get_queryset())
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

    @decorators.action("put", detail=True)
    def extend_date(self, request, pk=None):
        pass


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
