from datetime import datetime

from rest_framework import mixins, permissions, request, viewsets

from product import models, serializers


class RequestExtendDate:
    @staticmethod
    def new_data(request: request.Request) -> request.Request:
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
