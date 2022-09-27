from rest_framework import viewsets

from . import models, serializers


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """

    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
