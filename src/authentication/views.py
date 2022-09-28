from rest_framework import viewsets

from . import models, serializers


class AttendantProfileViewSet(viewsets.ModelViewSet):
    queryset = models.AttendantProfile.objects.all()
    serializer_class = serializers.AttendantProfileSerializer
