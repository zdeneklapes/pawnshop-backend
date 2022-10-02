from rest_framework import mixins, viewsets, permissions

from . import models, serializers


class UserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]  # TODO: Uncomment


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
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]  # TODO: Uncomment
