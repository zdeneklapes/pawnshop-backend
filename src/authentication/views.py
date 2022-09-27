from rest_framework import viewsets

from . import models, serializers


class UserViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
