"""Create your announcement url routing here."""
from django.urls import path

from . import views

app_name = "announcement"

urlpatterns = [
    path(
        "",
        views.AnnouncementView.as_view(extra_context={"title": "Announcement"}),
        name="announcement",
    )
]
