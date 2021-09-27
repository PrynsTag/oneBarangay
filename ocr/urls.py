"""URL Routing for OCR."""
from django.urls import path

from . import views

urlpatterns = [
    path("upload", views.FileUploadView.as_view(), name="upload"),
    path("files", views.ScanFileView.as_view(), name="files"),
    path("ocr_files", views.OCRFilesView.as_view(), name="ocr_files"),
    path(
        "scan_result/<str:filename>",
        views.ScanResultView.as_view(),
        name="scan_result",
    ),
    path("save_result", views.SaveScanResultView.as_view(), name="save_result"),
    path("", views.RBITableView.as_view(), name="rbi_table"),
    path("rbi", views.RBIView.as_view(), name="rbi"),
    path(
        "<str:page>/<str:created_at>/",
        views.RBIView.as_view(),
        name="rbi",
    ),
]
