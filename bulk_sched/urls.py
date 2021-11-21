"""Create your bulk_sched url routing here."""
from django.urls import path

from . import views

app_name = "bulk_sched"

urlpatterns = [
    path(
        "bulk-sched/create",
        views.BulkSchedCreateView.as_view(),
        name="create",
    ),
    path(
        "bulk-sched/home",
        views.BulkSchedHomeView.as_view(),
        name="home",
    ),
    path(
        "cedula",
        views.CedulaCreateView.as_view(),
        name="cedula",
    ),
]
