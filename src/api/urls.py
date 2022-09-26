from django.urls import path

from . import views

urlpatterns = [
    # path("", viewsets_user.cocktail_list),
    path("users/", views.UserView.as_view()),
    path("users/<int:pk>", views.UserIdView.as_view()),
]
