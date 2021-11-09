"""OCR Forms."""
from datetime import datetime

from django import forms

from one_barangay.validators import validate_extension
from one_barangay.widgets import DatePickerWidget, DropzoneWidget

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

GENDER_CHOICES = (
    ("Male", "Male"),
    ("Femaile", "Female"),
    ("Others", "Others"),
)

CIVIL_STATUS_CHOICES = (
    ("Married", "Married"),
    ("Widowed", "Widowed"),
    ("Separated", "Separated"),
    ("Divorced", "Divorced"),
    ("Single", "Single"),
)


class OcrUploadForm(forms.Form):
    """Upload Form."""

    error_css_class = "is-invalid"
    required_css_class = "required"

    file_upload = forms.FileField(
        validators=[validate_extension],
        label="",
        widget=DropzoneWidget(
            attrs={
                "class": "",
                "accept": "image/jpeg,image/png,image/jpg,application/pdf",
                "multiple": True,
            }
        ),
    )


class OcrEditForm(forms.Form):
    """Edit form for OCR."""

    error_css_class = "is-invalid"
    required_css_class = "required"

    house_num = forms.CharField(
        label="House Number",
        label_suffix="",
        widget=forms.HiddenInput(attrs={"class": "form-control"}),
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


class OcrHouseForm(forms.Form):
    """House information form."""

    error_css_class = "is-invalid"
    required_css_class = "required"

    creation_date = forms.DateTimeField(
        label="",
        label_suffix="",
        widget=forms.HiddenInput(attrs={"class": "form-control"}),
    )
    region = forms.CharField(
        label="Region",
        label_suffix="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control text-black",
                "readonly": True,
            }
        ),
    )
    province = forms.CharField(
        label="Province",
        label_suffix="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control text-black",
                "readonly": True,
            }
        ),
    )
    city = forms.CharField(
        label="City",
        label_suffix="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control text-black",
                "readonly": True,
            }
        ),
    )
    barangay = forms.CharField(
        label="Barangay",
        label_suffix="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control text-black",
                "readonly": True,
            }
        ),
    )
    house_num = forms.CharField(
        label="House #",
        label_suffix="",
        widget=forms.TextInput(attrs={"class": "form-control text-black"}),
    )
    address = forms.CharField(
        label="Address",
        label_suffix="",
        widget=forms.TextInput(attrs={"class": "form-control text-black"}),
    )
    date_accomplished = forms.DateField(
        label="Date Filled",
        label_suffix="",
        input_formats=[
            "%Y-%m-%d",
            "%m/%d/%Y",
            "%m/%d/%y",
            "%b %d %Y",
            "%b %d, %Y",
            "%d %b %Y",
            "%d %b, %Y",
            "%B %d %Y",
            "%B %d, %Y",
            "%d %B %Y",
            "%d %B, %Y",
        ],
        widget=DatePickerWidget(
            attrs={
                "class": "form-control text-black date-picker",
                "autocomplete": "off",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        """Initialize OcrHouseForm fields."""
        super().__init__(*args, **kwargs)
        self.fields["creation_date"].initial = datetime.now()
        self.fields["region"].initial = "NCR"
        self.fields["province"].initial = "3rd District"
        self.fields["city"].initial = "Valenzuela"
        self.fields["barangay"].initial = "Malanday"


class OcrFamilyForm(forms.Form):
    """Family information form."""

    error_css_class = "is-invalid"
    required_css_class = "required"

    last_name = forms.CharField(
        label="Last Name",
        label_suffix="",
        widget=forms.TextInput(attrs={"class": "form-control text-black"}),
    )
    first_name = forms.CharField(
        label="First Name",
        label_suffix="",
        widget=forms.TextInput(attrs={"class": "form-control text-black"}),
    )
    middle_name = forms.CharField(
        label="Middle Name",
        label_suffix="",
        widget=forms.TextInput(attrs={"class": "form-control text-black"}),
    )
    ext = forms.CharField(
        label="Ext",
        label_suffix="",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control text-black"}),
    )
    place_of_birth = forms.CharField(
        label="Birth Place",
        label_suffix="",
        widget=forms.TextInput(attrs={"class": "form-control text-black"}),
    )
    date_of_birth = forms.DateField(
        label="Birth Date",
        label_suffix="",
        input_formats=[
            "%Y-%m-%d",
            "%m/%d/%Y",
            "%m/%d/%y",
            "%b %d %Y",
            "%b %d, %Y",
            "%d %b %Y",
            "%d %b, %Y",
            "%B %d %Y",
            "%B %d, %Y",
            "%d %B %Y",
            "%d %B, %Y",
        ],
        widget=DatePickerWidget(
            attrs={"class": "form-control text-black date-picker", "autocomplete": "off"}
        ),
    )
    gender = forms.ChoiceField(
        label="Gender",
        label_suffix="",
        widget=forms.Select(
            attrs={
                "class": "form-select text-black",
                "aria-label": "Street Select",
            },
        ),
        choices=GENDER_CHOICES,
    )
    civil_status = forms.ChoiceField(
        label="Civil Status",
        label_suffix="",
        widget=forms.Select(
            attrs={
                "class": "form-select text-black",
                "aria-label": "Street Select",
            },
        ),
        choices=CIVIL_STATUS_CHOICES,
    )
    citizenship = forms.CharField(
        label_suffix="",
        widget=forms.TextInput(attrs={"class": "form-control text-black"}),
    )
    monthly_income = forms.IntegerField(
        label_suffix="",
        min_value=0,
        widget=forms.NumberInput(attrs={"class": "form-control text-black"}),
    )
    remarks = forms.CharField(
        label_suffix="",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control text-black"}),
    )

    def __init__(self, *args, **kwargs):
        """Initialize OcrFamilyForm fields."""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if self.fields[field].required:
                self.fields[field].widget.attrs["required"] = True
