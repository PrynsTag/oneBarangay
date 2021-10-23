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
    path("user_verify/<str:document_id>", views.user_verify, name="user_verify"),
    path(
        "id_verification_manual/<str:user_uid>/<str:document_id>",
        views.id_verification_manual,
        name="id_verification_manual",
    ),
    path(
        "appointment_resched/<str:document_id>/<str:url_date>",
        views.appointment_resched,
        name="appointment_resched",
    ),
    path("user_resched/<str:document_id>", views.user_resched, name="user_resched"),
    path("process/<str:document_id>", views.process, name="process"),
    path(
        "document_data/<str:document_id>/<str:document_name>",
        views.document_data,
        name="document_data",
    ),
    path(
        "document_data_edit/<str:document_id>/<str:document_name>",
        views.document_data_edit,
        name="document_data_edit",
    ),
    path(
        "create_document/<str:document_id>/<str:document_name>",
        views.create_document,
        name="create_document",
    ),
    path(
        "confirm_document_data/<str:document_id>",
        views.confirm_document_data,
        name="confirm_document_data",
    ),
    path(
        "remove_document_session/<str:date>",
        views.remove_document_session,
        name="remove_document_session",
    ),
    path("get/<str:document_id>", views.get, name="get"),
    path("add_appointment", views.add_appointment, name="add_appointment"),
    path(
        "add_appointment_manual/<int:year>/<int:month>/<int:day>",
        views.add_appointment_manual,
        name="add_appointment_manual",
    ),
    path("delete_account", views.delete_account, name="delete_account"),
    path(
        "available/<str:old_document_id>/<str:new_document_id>", views.available, name="available"
    ),
    path(
        "schedule_get_document/<str:document_id>/<str:url_date>",
        views.get_document_resched,
        name="get_document_resched",
    ),
    path(
        "issue_document_resched/<str:document_id>",
        views.issue_document_resched,
        name="issue_document_resched",
    ),
]
