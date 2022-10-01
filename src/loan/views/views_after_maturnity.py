from rest_framework import mixins, permissions, viewsets

from loan import models, serializers


class LoanListAfterMaturityViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.Loan.objects.after_maturity()
    serializer_class = serializers.LoanSerializer
    permission_classes = [permissions.IsAuthenticated]
