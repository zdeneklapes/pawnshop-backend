from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("all", views.StatisticAllViewSet)
router.register("daily", views.StatisticDailyViewSet)
router.register("reset", views.StatisticResetViewSet)
urlpatterns = [path("", include(router.urls))]
