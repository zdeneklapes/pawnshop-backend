from rest_framework import permissions, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from . import models, serializers
from config.settings import AUTH


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser] if AUTH else [permissions.AllowAny]
    http_method_names = ["get", "patch"]


class AttendantProfileViewSet(viewsets.ModelViewSet):
    queryset = models.AttendantProfile.objects.all()
    serializer_class = serializers.AttendantProfileSerializer
    permission_classes = [permissions.IsAuthenticated] if AUTH else [permissions.AllowAny]
    http_method_names = ["get", "post", "patch"]


# class AttendantProfileCreateViewSet(viewsets.ModelViewSet):
#     queryset = models.AttendantProfile.objects.all()
#     serializer_class = serializers.RegisterSerializer
#     permission_classes = [permissions.IsAuthenticated] if AUTH else [permissions.AllowAny]
#     http_method_names = ["post"]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer
