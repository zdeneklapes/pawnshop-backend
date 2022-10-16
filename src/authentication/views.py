from rest_framework import mixins, viewsets, permissions
from rest_framework_simplejwt.views import TokenObtainPairView

from . import models, serializers


class UserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]  # TODO: Uncomment


class AttendantProfileCreateViewSet(viewsets.ModelViewSet):
    queryset = models.AttendantProfile.objects.all()
    serializer_class = serializers.AttendantProfileSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]  # TODO: Uncomment
    http_method_names = ["get", "post", "patch", "delete"]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer
