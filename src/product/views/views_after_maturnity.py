from rest_framework import mixins, permissions, viewsets

from product import models, serializers


class LoanListAfterMaturityViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.Loan.objects.after_maturity()
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
