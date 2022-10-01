from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenVerifyView

from . import views

# Automatically find all url based on ViewSet (all?)
router = routers.DefaultRouter()
router.register(prefix=r"users", viewset=views.UserViewSet)
router.register(prefix=r"attendants", viewset=views.AttendantProfileCreateViewSet)
router.register(prefix=r"customers", viewset=views.CustomerProfileViewSet)

urlpatterns = [
    # Authentication
    path("", include(router.urls)),
    # Tokens
    path("token/create/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
