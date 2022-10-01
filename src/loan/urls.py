from rest_framework.routers import DefaultRouter

from .views import views_base
from .views import views_after_maturnity
from .views import views_extend_date

router = DefaultRouter()
router.register(prefix=r"", viewset=views_base.LoanViewSet)
router.register(
    prefix=r"after-maturity", viewset=views_after_maturnity.LoanListAfterMaturityViewSet
)
router.register(
    prefix=r"extend-date", viewset=views_extend_date.LoanPartialUpdateExtendDateViewSet
)
urlpatterns = router.urls
