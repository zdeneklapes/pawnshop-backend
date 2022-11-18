from rest_framework import routers

from . import views

#
router = routers.DefaultRouter()
router.register(prefix=r"", viewset=views.CustomerProfileViewSet)

#
urlpatterns = router.urls
