"""URL Routing for OCR."""
from django.urls import path

from . import views

app_name = "ocr"

urlpatterns = [
    # OCR Table Section
    path(
        "",
        views.OcrHomeView.as_view(),
        name="home",
    ),
    path(
        "edit/<str:house_num>",
        views.OcrEditView.as_view(),
        name="edit",
    ),
    path(
        "delete/<str:house_num>",
        views.delete,
        name="delete",
    ),
    path(
        "detail/<str:house_num>",
        views.OcrDetailView.as_view(),
        name="detail",
    ),
    # OCR Scan Section
    path(
        "upload",
        views.OcrFileUploadView.as_view(),
        name="upload",
    ),
    path(
        "remove/<str:filename>",
        views.remove_file,
        name="remove_file",
    ),
    path(
        "scan_result/<str:filename>",
        views.OcrResultView.as_view(),
        name="scan_result",
    ),
    path(
        "save_result",
        views.OcrSaveView.as_view(),
        name="save_result",
    ),
]
