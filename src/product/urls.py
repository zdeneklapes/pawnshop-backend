from rest_framework.routers import DefaultRouter

# from .views import views_after_maturnity
# from .views import views_extend_date
from . import views

router = DefaultRouter()
router.register(prefix=r"", viewset=views.CreateProductViewSet)
router.register(prefix=r"loans", viewset=views.LoanViewSet)
router.register(prefix=r"offers", viewset=views.OfferViewSet)
router.register(prefix=r"after-maturity", viewset=views.AfterMaturityViewSet)

router.register(prefix=r"extend-loan", viewset=views.ExtendDateViewSet)
router.register(prefix=r"return-loan", viewset=views.ReturnLoanViewSet)
router.register(prefix=r"loan-to-bazar", viewset=views.LoanToBazarViewSet)

urlpatterns = router.urls
