"""URLConfig for data_viz."""
from django.urls import path

from . import views

app_name = "data_viz"

urlpatterns = [path("", views.DataVizView.as_view(), name="dashboard")]
