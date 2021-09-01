"""URL Routing for OCR."""
from django.urls import re_path

from . import views

urlpatterns = [re_path(r"^.*\.html", views.ocr_pages, name="ocr-pages")]
