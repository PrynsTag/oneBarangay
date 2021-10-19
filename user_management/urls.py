"""Create your URL Routing for authentication here."""
from django.urls import path

from . import views

app_name = "user_management"

urlpatterns = [
    path(
        "",
        views.AddUserFormView.as_view(),
        name="user_management",
    ),
    path(
        "edit_user",
        views.EditUserFormView.as_view(),
        name="edit_user",
    ),
    path(
        "delete_user",
        views.DeleteUserFormView.as_view(),
        name="delete_user",
    ),
]
