from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema

from authentication.models import User, UserGroupChoice
from authentication.serializers.admin import AdminSerializer
from config.settings import AUTH
from authentication.views.swaggers.base import AttendantQPSwagger
from authentication.views.permissions import AuthenticationPermission


@method_decorator(name="create", decorator=swagger_auto_schema(request_body=AttendantQPSwagger.create))
@method_decorator(name="partial_update", decorator=swagger_auto_schema(request_body=AttendantQPSwagger.update))
class AdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [permissions.IsAuthenticated, AuthenticationPermission] if AUTH else [permissions.AllowAny]
    http_method_names = ["get", "patch", "delete"]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.role in [UserGroupChoice.ADMIN.name]:
            return Response(data={"detail": "Admin can't be deleted"}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
