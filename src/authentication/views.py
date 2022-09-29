from rest_framework import status, viewsets
from rest_framework.response import Response

from . import models, serializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


# class AttendantProfileCreateView(generics.GenericAPIView):
class AttendantProfileCreateViewSet(viewsets.ModelViewSet):
    queryset = models.AttendantProfile.objects.all()
    serializer_class = serializers.AttendantProfileSerializer

    # permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerProfileViewSet(viewsets.ModelViewSet):
    queryset = models.CustomerProfile.objects.all()
    serializer_class = serializers.CustomerProfileSerializer
