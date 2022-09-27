import requests
from django.urls import path

# from . import views

urlpatterns = [
    path(
        "user/",
        lambda req: requests.get("https://jsonplaceholder.typicode.com/posts/1"),
    ),
    # path("users/", views.UserView.as_view()),
    # path("users/<int:pk>", views.UserIdView.as_view()),
]
