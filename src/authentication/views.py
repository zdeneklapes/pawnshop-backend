from rest_framework import generics, status
from rest_framework.response import Response

from . import models, serializers


class UserView(generics.GenericAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class AttendantProfileCreateView(generics.GenericAPIView):
    # queryset = models.AttendantProfile.objects.all()
    serializer_class = serializers.AttendantProfileSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerProfileView(generics.GenericAPIView):
    queryset = models.CustomerProfile.objects.all()
    serializer_class = serializers.CustomerProfileSerializer
