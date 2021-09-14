"""OCR Forms."""
from django import forms
from django.forms import ClearableFileInput

from .models import Upload


class UploadForm(forms.ModelForm):
    """Upload Form."""

    class Meta:
        """Meta Class."""

        model = Upload
        fields = ["upload_file"]
        labels = {"upload_file": "File:"}
        widgets = {
            "upload_file": ClearableFileInput(attrs={"multiple": True}),
        }
