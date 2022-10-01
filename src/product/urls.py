from rest_framework.routers import DefaultRouter

from .views import views_base
# from .views import views_after_maturnity
# from .views import views_extend_date

router = DefaultRouter()
router.register(prefix=r"loans", viewset=views_base.LoanViewSet)
router.register(prefix=r"offers", viewset=views_base.OfferViewSet)
router.register(prefix=r"after-maturity", viewset=views_base.AfterMaturityViewSet)
urlpatterns = router.urls
