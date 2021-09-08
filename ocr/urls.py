"""URL Routing for OCR."""
from django.urls import path

from . import views

urlpatterns = [
    path("upload", views.FileUploadView.as_view(), name="upload"),
    path("files", views.ScanFileView.as_view(), name="files"),
    path(
        "scan_result/<str:filename>",
        views.ScanResultView.as_view(),
        name="scan_result",
    ),
]
