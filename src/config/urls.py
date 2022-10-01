from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainSlidingView, TokenRefreshSlidingView

schema_view = get_schema_view(
    openapi.Info(
        title="Pawnshop API",
        default_version="v1",
        description="A REST API for a Pawnshop system",
        contact=openapi.Contact(email="lapes.zdenek@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]

urlpatterns += [
    #
    path("admin/", admin.site.urls),
    path("authentication/", include("djoser.urls.jwt")),
    # path('api/token/', TokenObtainSlidingView.as_view(), name='token_obtain'),
    # path('api/token/refresh/', TokenRefreshSlidingView.as_view(), name='token_refresh'),
    #
    path("authentication/", include("authentication.urls")),
    path("product/", include("product.urls")),
    # path("cashdesk/", include("cashdesk.urls")), # Note: It doesn't need routing
    # path("loans/", include("product.urls")),
    # path("offers/", include("offer.urls")),
    # path("products/", include("products.urls")),  # Note: It doesn't need routing
    path("shop/", include("shop.urls")),
    path("statistics/", include("statistic.urls")),
]
