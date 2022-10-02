from rest_framework import mixins, viewsets

from . import models, serializers


class UserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    # permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser] # TODO: Uncomment


class AttendantProfileCreateViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.AttendantProfile.objects.all()
    serializer_class = serializers.AttendantProfileSerializer
    # permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser] # TODO: Uncomment


class CustomerProfileViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = models.CustomerProfile.objects.all()
    serializer_class = serializers.CustomerProfileSerializer
    # permission_classes = [permissions.IsAuthenticated] # TODO: Uncomment
