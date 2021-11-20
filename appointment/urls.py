"""URL Routing for Appointment."""
from django.urls import path

from . import views

app_name = "appointment"


# class DateConverter:
#     regex = "\d{4}-\d{2}-\d{2}"
#
#     def to_python(self, value):
#         return datetime.datetime.strptime(value, "%Y-%m-%d")
#
#     def to_url(self, value):
#         return value
#
#
# register_converter(DateConverter, "yyyy")

urlpatterns = [
    path("document/request/", views.document_request, name="document_request"),
    path(
        "user/verification/<str:document_request_id>",
        views.user_document_verification,
        name="user_document_verification",
    ),
    path(
        "user/document/cancel/",
        views.user_document_cancel,
        name="document_cancel",
    ),
    path(
        "user/document/cancel/<str:document_request_id>",
        views.user_document_cancel,
        name="document_cancel",
    ),
    path(
        "user/dummy/appointment/<int:account_num>",
        views.add_document_request,
        name="add_document_request",
    ),
    path(
        "user/document/request/verified/",
        views.user_document_verification,
        name="document_request_verified",
    ),
    path(
        "user/document/request/verified/<str:document_request_id>/<str:user_id>",
        views.document_request_verified,
        name="document_request_verified",
    ),
    path(
        "user/document/issuing/list/<str:document_request_id>/<str:user_id>",
        views.user_issuing_list,
        name="user_issuing_list",
    ),
    path(
        "user/document/issuing/success/<str:document_id>/<str:document_slugify>",
        views.document_issuing_success,
        name="document_issuing_success",
    ),
    path(
        "user/document/issuing/process/<str:document_request_id>/<str:document_slugify>",
        views.document_issuing_process,
        name="document_issuing_process",
    ),
    path(
        "user/document/request/verification/<str:document_request_id>",
        views.user_verification_dt,
        name="user_verification_dt",
    ),
    path(
        "user/verification/selection/<str:document_request_id>",
        views.user_selection_data,
        name="user_selection_data",
    ),
    path("user/verification/selection/filter", views.user_filter, name="user_filter"),
    path(
        "user/document/info/<str:document_request_id>/<str:document_slugify>",
        views.document_input_info,
        name="document_input_info",
    ),
    path(
        "user/document/process/status/<str:document_request_id>",
        views.document_process_change_status,
        name="document_process_change_status",
    ),
]
