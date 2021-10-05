"""URL Routing for Appointment."""
from django.urls import path

from . import views

app_name = "appointment"

urlpatterns = [
    path("view_appointments/<str:date>", views.view_appointments, name="view_appointments"),
    path(
        "request/<str:document_id>",
        views.request,
        name="request",
    ),
    path(
        "id_verification/<str:document_id>",
        views.id_verification,
        name="id_verification",
    ),
    path("user_verified/<str:document_id>", views.user_verified, name="user_verified"),
    path(
        "id_verification_manual/<str:user_uid>",
        views.id_verification_manual,
        name="id_verification_manual",
    ),
    path(
        "appointment_resched/<str:document_id>/<str:url_date>",
        views.appointment_resched,
        name="appointment_resched",
    ),
    path("process/<str:document_id>", views.process, name="process"),
    path("get/<str:document_id>", views.get, name="get"),
    path("add_appointment", views.add_appointment, name="test_appointment"),
    path("delete_account", views.delete_account, name="delete_account"),
    path(
        "available/<str:old_document_id>/<str:new_document_id>", views.available, name="available"
    ),
]
