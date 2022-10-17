from rest_framework import mixins, viewsets, permissions

from . import models, serializers
from config.settings import AUTH


class CustomerProfileViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.CustomerProfile.objects.all()
    serializer_class = serializers.CustomerProfileSerializer
    permission_classes = [permissions.IsAuthenticated] if AUTH else [permissions.AllowAny]
