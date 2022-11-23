from rest_framework.response import Response
from rest_framework import generics, permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView

from authentication.serializers.token import CustomTokenObtainPairSerializer, LogoutAllSerializer
from statistic.serializers.statistic import StatisticSerializer
from statistic.models.models import StatisticDescription


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response


class LogoutAllView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LogoutAllSerializer

    def post(self, request):
        StatisticSerializer.save_statistic_auth_create(StatisticDescription.LOGOUT.name, request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
