from django.urls import path, re_path

from . import views

urlpatterns = [
    # The home page
    path("ocr", views.index, name="ocr-home"),
    re_path(r"^.*\.*", views.ocr, name="ocr-pages"),
]
