from django.contrib import admin
from django.urls import include, path, re_path

# from drf_yasg import openapi
# from drf_yasg.views import get_schema_view
# from rest_framework import permissions
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenVerifyView

# schema_view = get_schema_view(
#     openapi.Info(
#         title="Pawnshop API",
#         default_version="v1",
#         description="A REST API for a Pawnshop system",
#         contact=openapi.Contact(email="lapes.zdenek@gmail.com"),
#         license=openapi.License(name="BSD License"),
#     ),
#     public=True,
#     permission_classes=[permissions.AllowAny],
# )
# from rest_framework_swagger.views import get_swagger_view
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    re_path(r"^swagger/$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    re_path(r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

urlpatterns += [
    # Admin
    path("admin/", admin.site.urls),
    # Swagger
    # path("swagger_download/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    # path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    # path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # Tokens
    path("token/create/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    # Apps
    path("authentication/", include("authentication.urls")),
    path("product/", include("product.urls")),
    path("shop/", include("shop.urls")),
    path("statistics/", include("statistic.urls")),
]
