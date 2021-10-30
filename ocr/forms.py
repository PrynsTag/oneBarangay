"""OCR Forms."""
from django import forms

STREET_CHOICES = (
    ("A. Duque", "A. Duque"),
    ("Aca Road", "Aca Road"),
    ("Bangcal Extension", "Bangcal Extension"),
    ("Bartolome Street", "Bartolome Street"),
    ("C. Molina Street", "C. Molina Street"),
    ("Central Road", "Central Road"),
    ("Cherry Blossom Street", "Cherry Blossom Street"),
    ("Dr. Bartolome", "Dr. Bartolome"),
    ("East Road", "East Road"),
    ("F. San Diego Street", "F. San Diego Street"),
    ("I. Fernando", "I. Fernando"),
    ("I. Lozada Street", "I. Lozada Street"),
    ("Jollibee Drive-Through", "Jollibee Drive-Through"),
    ("M.H. del Pilar Footbridge (footway)", "M.H. del Pilar Footbridge (footway)"),
    ("Main Road", "Main Road"),
    ("North Road", "North Road"),
    ("Orange Street", "Orange Street"),
    ("P. Adriano", "P. Adriano"),
    ("Peach Street", "Peach Street"),
    ("Road 1", "Road 1"),
    ("Roseville Street", "Roseville Street"),
    ("South RoadSt. Elsewhere Street", "South RoadSt. Elsewhere Street"),
    ("T. Santiago Street", "T. Santiago Street"),
    ("West Road", "West Road"),
)


class UploadForm(forms.Form):
    """Upload Form."""

    error_css_class = "is-invalid"
    required_css_class = "required"

    upload_file = forms.FileField(
        label="File:", widget=forms.ClearableFileInput(attrs={"multiple": True})
    )


class OcrEditForm(forms.Form):
    """Edit form for OCR."""

    error_css_class = "is-invalid"
    required_css_class = "required"

    house_num = forms.CharField(
        label="House Number",
        label_suffix="",
        widget=forms.HiddenInput(),
    )
    address = forms.CharField(
        label_suffix="",
        label="Home Address",
        widget=forms.TextInput(
            attrs={
                "class": "form-control text-black",
            }
        ),
    )
    street = forms.ChoiceField(
        label_suffix="",
        label="Street Address",
        widget=forms.Select(
            attrs={
                "class": "form-select text-black",
                "aria-label": "Street Select",
            },
        ),
        choices=STREET_CHOICES,
    )

    def __init__(self, *args, rbi=None, **kwargs):
        """Initialize OcrEditForm form field value."""
        super().__init__(*args, **kwargs)

        for field in self.fields:
            if rbi is not None:
                self.fields[field].initial = rbi.get(field)
