"""OCR Forms."""

from django import forms


class UploadForm(forms.Form):
    """Upload Form."""

    upload_file = forms.FileField(
        label="File:", widget=forms.ClearableFileInput(attrs={"multiple": True})
    )
