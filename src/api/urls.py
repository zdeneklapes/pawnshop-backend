from django.urls import include, path

from .viewsets import viewsets_user

urlpatterns = [
    path("", viewsets_user.cocktail_list),
]
