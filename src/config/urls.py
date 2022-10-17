from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from config.settings import AUTH

schema_view = get_schema_view(
    openapi.Info(
        title="Pawnshop API",
        default_version="v1",
        description="A REST API for a Pawnshop system",
        contact=openapi.Contact(email="lapes.zdenek@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.IsAuthenticated] if AUTH else [permissions.AllowAny],
)

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # Swagger
    path("swagger_download/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # Apps
    path("authentication/", include("authentication.urls")),
    path("customer/", include("customer.urls")),
    path("product/", include("product.urls")),
    path("shop/", include("shop.urls")),
    path("statistic/", include("statistic.urls")),
]
