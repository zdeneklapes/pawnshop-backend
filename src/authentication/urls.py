from django.urls import include, path
from rest_framework import routers

from . import views

# Automatically find all url based on ViewSet (all?)
router = routers.DefaultRouter()
router.register(prefix=r"users", viewset=views.UserViewSet)
router.register(prefix=r"attendants", viewset=views.AttendantProfileCreateViewSet)
router.register(prefix=r"customers", viewset=views.CustomerProfileViewSet)

urlpatterns = [path("", include(router.urls))]
