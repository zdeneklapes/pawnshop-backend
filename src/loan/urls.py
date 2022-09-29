from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(prefix=r"", viewset=views.LoanViewSet)
urlpatterns = router.urls
