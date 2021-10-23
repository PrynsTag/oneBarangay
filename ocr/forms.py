"""OCR Forms."""
from django import forms


class UploadForm(forms.Form):
    """Upload Form."""

    error_css_class = "is-invalid"
    required_css_class = "required"

    upload_file = forms.FileField(
        label="File:", widget=forms.ClearableFileInput(attrs={"multiple": True})
    )
