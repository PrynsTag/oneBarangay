from django.urls import path

from ocr import views

urlpatterns = [
    # The home page
    path("", views.index, name="home"),
    path("ocr", views.ocr, name="ocr-views"),
]
