"""Create your announcement url routing here."""
from django.urls import path

from . import views

app_name = "announcement"

urlpatterns = [
    path(
        "",
        views.AnnouncementHomeView.as_view(),
        name="home",
    ),
    path(
        "create/",
        views.AnnouncementCreateView.as_view(),
        name="create",
    ),
    path(
        "edit/<slug:announcement_id>/",
        views.AnnouncementEditView.as_view(),
        name="edit",
    ),
    path(
        "delete/<slug:announcement_id>/<str:thumbnail_name>",
        views.delete,
        name="delete",
    ),
    path(
        "view/<slug:announcement_id>/",
        views.AnnouncementDetailView.as_view(),
        name="view",
    ),
]
