from django.urls import path

from . import views

# Automatically find all url based on ViewSet (all?)
# router = DefaultRouter()
# router.register(prefix=r"signup", viewset=views.AttendantProfileCreateView.as_view())

urlpatterns = [path("signup/", views.AttendantProfileCreateView.as_view())]
