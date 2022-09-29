from rest_framework import routers

from . import views

# Automatically find all url based on ViewSet (all?)
router = routers.DefaultRouter()
router.register(prefix=r"signup", viewset=views.AttendantProfileCreateViewSet)

urlpatterns = (
    router.urls
)  # [path("signup/", views.AttendantProfileCreateView.as_view())]
