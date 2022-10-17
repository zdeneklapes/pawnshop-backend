from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema

from authentication.models import AttendantProfile, User, UserRoleChoice
from authentication.serializers.user import UserSerializer, AttendantProfileSerializer, CustomTokenObtainPairSerializer
from config.settings import AUTH
from authentication.views.swaggers.user import AttendantQPSwagger


@method_decorator(name="create", decorator=swagger_auto_schema(request_body=AttendantQPSwagger.create))
@method_decorator(name="partial_update", decorator=swagger_auto_schema(request_body=AttendantQPSwagger.update))
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser] if AUTH else [permissions.AllowAny]
    http_method_names = ["get", "patch", "delete"]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.role in [UserRoleChoice.ADMIN.name]:
            return Response(data={"detail": "Admin can't be deleted"}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


@method_decorator(name="create", decorator=swagger_auto_schema(request_body=AttendantQPSwagger.create))
@method_decorator(name="partial_update", decorator=swagger_auto_schema(request_body=AttendantQPSwagger.update))
class AttendantProfileViewSet(viewsets.ModelViewSet):
    queryset = AttendantProfile.objects.all()
    serializer_class = AttendantProfileSerializer
    permission_classes = [permissions.IsAuthenticated] if AUTH else [permissions.AllowAny]
    http_method_names = ["get", "post", "patch"]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
