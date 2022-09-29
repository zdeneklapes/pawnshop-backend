from rest_framework import mixins, viewsets


# Source: https://stackoverflow.com/q/45414928/14471542
class StatisticViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Just bundle all serializers.data and send Response with all data"""

    serializer_class_authentication = None
    serializer_class_cashdesk = None
    serializer_class_loan = None
    serializer_class_offer = None
    serializer_class_product = None
    serializer_class_shop = None

    def list(self, request, *args, **kwargs):
        pass
