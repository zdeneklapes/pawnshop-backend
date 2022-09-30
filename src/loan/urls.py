from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(prefix=r"", viewset=views.LoanViewSet)
router.register(prefix=r"after-maturity", viewset=views.LoanAfterMaturityViewSet)
router.register(prefix=r"extend-date", viewset=views.LoanExtendDateViewSet)
urlpatterns = router.urls
