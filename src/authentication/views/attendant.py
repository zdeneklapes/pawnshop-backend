from rest_framework import permissions, viewsets
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema

from authentication.models import AttendantProfile
from authentication.serializers.attendant import AttendantProfileSerializer
from config.settings import AUTH
from authentication.views.swaggers.base import AttendantQPSwagger


# TODO: Attendant Login/Logout Statistics Record


@method_decorator(name="create", decorator=swagger_auto_schema(request_body=AttendantQPSwagger.create))
@method_decorator(name="partial_update", decorator=swagger_auto_schema(request_body=AttendantQPSwagger.update))
class AttendantProfileViewSet(viewsets.ModelViewSet):
    queryset = AttendantProfile.objects.all()
    serializer_class = AttendantProfileSerializer
    permission_classes = [permissions.IsAuthenticated] if AUTH else [permissions.AllowAny]
    http_method_names = ["get", "post", "patch"]
