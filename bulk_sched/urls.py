"""Create your bulk_sched url routing here."""
from django.urls import path

from . import views

app_name = "bulk_sched"

urlpatterns = [
    path(
        "bulk-sched",
        views.BulkSchedCreateView.as_view(),
        name="create",
    ),
    path(
        "cedula",
        views.CedulaCreateView.as_view(),
        name="cedula",
    ),
]
