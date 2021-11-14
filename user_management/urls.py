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
        "edit/<str:user_id>",
        views.UserManagementEditView.as_view(),
        name="edit",
    ),
    path(
        "delete/<str:user_id>",
        views.delete,
        name="delete",
    ),
    path(
        "reset/<str:email>",
        views.reset,
        name="reset",
    ),
]
