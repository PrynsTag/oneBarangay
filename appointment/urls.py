"""URL Routing for Appointment."""
from django.urls import path

from . import views

app_name = "appointment"

urlpatterns = [
    path(
        "view-appointment/<str:date>", views.view_appointment, name="view-appointment"
    ),
    path(
        r"detail-appointment/<str:document_id>",
        views.details_appointment,
        name="detail-appointment",
    ),
    path(
        "id_verification/<str:document_id>",
        views.id_verification,
        name="id_verification",
    ),
    path("user_verified/<str:document_id>", views.user_verified, name="user_verified"),
    path("add_appointment", views.add_appointment, name="test_appointment"),
    path("delete_account", views.delete_account, name="delete_account"),
]
