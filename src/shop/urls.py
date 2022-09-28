from rest_framework.routers import DefaultRouter

from . import views

# Automatically find all url based on ViewSet (all?)
router = DefaultRouter()
router.register(prefix=r"", viewset=views.ShopViewSet)

urlpatterns = router.urls
