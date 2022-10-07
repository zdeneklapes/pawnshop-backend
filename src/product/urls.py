from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views.product import ProductViewSet, ContractPdf

router = DefaultRouter()
router.register(prefix=r"", viewset=ProductViewSet)

urlpatterns = [
    path("contract/", ContractPdf.as_view()),
    # path("contract/", PDFTemplateView.as_view(template_name='documents/loan_contract.html')),
    path("", include(router.urls)),
]
