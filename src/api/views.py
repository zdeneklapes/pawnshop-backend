import requests
from django.http import JsonResponse
from rest_framework import generics

from . import models, serializers


class UserView(generics.GenericAPIView):
    serializer_class = serializers.UserSerializer


class UserIdView(generics.GenericAPIView):
    pass
