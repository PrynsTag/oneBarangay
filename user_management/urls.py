"""Create your URL Routing for authentication here."""
from django.urls import path

from . import views

app_name = "user_management"

urlpatterns = [
    path(
        "",
        views.UserManagementHomeView.as_view(),
        name="home",
    ),
    path(
        "edit",
        views.UserManagementEditView.as_view(),
        name="edit",
    ),
    path(
        "delete",
        views.delete,
        name="delete",
    ),
    path(
        "reset",
        views.reset,
        name="reset",
    ),
]
