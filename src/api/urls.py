from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', include("myapp.urls")),
    path('', include("django_nextjs.urls")),
]
