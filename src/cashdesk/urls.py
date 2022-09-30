from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(prefix=r"", viewset=views.CashDeskViewSet)
urlpatterns = router.urls
