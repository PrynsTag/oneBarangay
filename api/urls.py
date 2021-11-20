"""URLConfig for api."""
from django.urls import path

from . import views

urlpatterns = [
    path("data_viz/", views.DataVizApiView.as_view()),
    path("ocr/<str:filename>", views.OcrApiView.as_view()),
    path("notification/", views.SendNotification.as_view()),
]
