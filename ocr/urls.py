"""URL Routing for OCR."""
from django.urls import path

from . import views
from .views import FileUploadView

urlpatterns = [
    path("upload", FileUploadView.as_view(), name="upload"),
    path("files", views.scan_file, name="files"),
    path("scan_result/<str:name>", views.scan_result, name="scan_result"),
]
