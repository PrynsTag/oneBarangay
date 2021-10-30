"""URL Routing for OCR."""
from django.urls import path

from . import views

app_name = "ocr"

urlpatterns = [
    path("", views.OcrHomeView.as_view(), name="home"),
    path("edit/<str:house_num>", views.OcrEditView.as_view(), name="edit"),
    path("delete/<str:house_num>", views.delete, name="delete"),
    path("detail/<str:house_num>", views.OcrDetailView.as_view(), name="detail"),
    path("upload", views.FileUploadView.as_view(), name="upload"),
    path("files", views.ScanFileView.as_view(), name="files"),
    path("ocr_files", views.OCRFilesView.as_view(), name="ocr_files"),
    path(
        "scan_result/<str:filename>",
        views.ScanResultView.as_view(),
        name="scan_result",
    ),
    path("save_result", views.SaveScanResultView.as_view(), name="save_result"),
]
