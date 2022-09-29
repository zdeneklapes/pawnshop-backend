from rest_framework import viewsets

from . import models, serializers


class LoanViewSet(viewsets.ModelViewSet):
    queryset = models.Loan.objects.all()
    serializer_class = serializers.LoanSerializer
