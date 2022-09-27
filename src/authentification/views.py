from rest_framework import generics

from . import serializers


class UserView(generics.GenericAPIView):
    serializer_class = serializers.UserSerializer


class UserIdView(generics.GenericAPIView):
    pass
