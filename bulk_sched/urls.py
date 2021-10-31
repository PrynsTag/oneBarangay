"""Create your bulk_sched url routing here."""
from django.urls import path

from . import views

app_name = "bulk_sched"

urlpatterns = [
    path(
        "",
        views.BulkSchedCreateView.as_view(),
        name="create",
    ),
]
