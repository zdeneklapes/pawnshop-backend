from rest_framework import mixins, viewsets

from . import models, serializers


class LoanViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Loan.objects.all()
    serializer_class = serializers.LoanSerializer
