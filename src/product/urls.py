from rest_framework.routers import DefaultRouter

from .views.product import (
    ProductViewSet,
    # CreateProductViewSet,
    # LoanViewSet,
    # OfferViewSet,
    # AfterMaturityViewSet,
    # ExtendLoanViewSet,
    # ReturnLoanViewSet,
    # LoanToBazarViewSet,
)

router = DefaultRouter()
router.register(prefix=r"", viewset=ProductViewSet)
# router.register(prefix=r"", viewset=CreateProductViewSet)
# router.register(prefix=r"extend-loan", viewset=ExtendLoanViewSet)
# router.register(prefix=r"return-loan", viewset=ReturnLoanViewSet)
# router.register(prefix=r"loan-to-bazar", viewset=LoanToBazarViewSet)

urlpatterns = router.urls


# router.register(prefix=r"loans", viewset=LoanViewSet)
# router.register(prefix=r"offers", viewset=OfferViewSet)
# router.register(prefix=r"after-maturity", viewset=AfterMaturityViewSet)
