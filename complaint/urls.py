"""Complaint urls."""
from django.urls import path

from . import views

app_name = "complaint"

urlpatterns = [path("", views.index, name="index")]
