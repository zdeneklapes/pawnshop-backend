from django.urls import include, path
from rest_framework import routers

from .views import statistic as statistic_views

router = routers.DefaultRouter()
router.register("", statistic_views.StatisticViewSet)
urlpatterns = [path("", include(router.urls))]
