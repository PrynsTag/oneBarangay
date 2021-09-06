"""URL Routing for OCR."""
from django.urls import path

from . import views

urlpatterns = [
    path("upload", views.file_upload, name="upload"),
    path("files", views.scan_file, name="files"),
    path("scan_file", views.scan_file, name="scan_file"),
]
