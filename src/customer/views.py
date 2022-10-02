from rest_framework import mixins, viewsets

from . import models, serializers


class CustomerProfileViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.CustomerProfile.objects.all()
    serializer_class = serializers.CustomerProfileSerializer
    # permission_classes = [permissions.IsAuthenticated] # TODO: Uncomment
