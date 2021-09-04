"""OCR Forms."""
from django import forms


class FileFieldForm(forms.Form):
    """Form for file upload."""

    file_field = forms.FileField(
        label="File",
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        required=False,
    )
