"""OCR Forms."""

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


class OcrResultForm(forms.Form):
    """Result form for OCR result."""

    error_css_class = "is-invalid"
    required_css_class = "required"

    region = forms.CharField(
        label="Region",
        label_suffix="",
        disabled=True,
        initial="NCR",
        widget=forms.TextInput(attrs={"class": "form-control text-black"}),
    )
    province = forms.CharField(
        label="Province",
        label_suffix="",
        disabled=True,
        initial="3rd District",
        widget=forms.TextInput(attrs={"class": "form-control text-black"}),
    )
    city = forms.CharField(
        label="City",
        label_suffix="",
        disabled=True,
        initial="Valenzuela City",
        widget=forms.TextInput(attrs={"class": "form-control text-black"}),
    )
    barangay = forms.CharField(
        label="Barangay",
        label_suffix="",
        disabled=True,
        initial="Malanday",
        widget=forms.TextInput(attrs={"class": "form-control text-black"}),
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
    date_filled = forms.DateField(
        label="Date Filled",
        label_suffix="",
        widget=DatePickerWidget(
            attrs={"class": "form-control text-black", "autocomplete": "off"}
        ),
    )
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
    extension = forms.CharField(
        label="Ext",
        label_suffix="",
        widget=forms.TextInput(attrs={"class": "form-control text-black"}),
    )
    place_of_birth = forms.CharField(
        label="Place of Birth",
        label_suffix="",
        widget=forms.TextInput(attrs={"class": "form-control text-black"}),
    )
    birth_date = forms.DateField(
        label="Date of Birth",
        label_suffix="",
        widget=DatePickerWidget(
            attrs={"class": "form-control text-black", "autocomplete": "off"}
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
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    remarks = forms.CharField(
        label_suffix="",
        widget=forms.TextInput(attrs={"class": "form-control text-black"}),
    )

    def __init__(self, *args, header=None, ocr_result=None, **kwargs):
        """Initialize OcrEditForm form field value."""
        super().__init__(*args, **kwargs)

        if not [var for var in (header, ocr_result) if var is None]:
            self.fields["region"].initial = "NCR"
            self.fields["province"].initial = "3rd District"
            self.fields["city"].initial = "Valenzuela City"
            self.fields["barangay"].initial = "Malanday"

            self.fields["house_num"].initial = header["household_no."]["text"]
            self.fields["address"].initial = header["address"]["text"]
            self.fields["date_filled"].initial = header["date"]["text"]

            self.fields["last_name"].initial = ocr_result["last_name_apelyido"]["text"]
            self.fields["first_name"].initial = ocr_result["first_name_pangalan"]["text"]
            self.fields["middle_name"].initial = ocr_result["middle_name"]["text"]
            self.fields["ext"].initial = ocr_result["ext"]["text"]
            self.fields["place_of_birth"].initial = ocr_result["place_of_birth"]["text"]
            self.fields["birth_date"].initial = ocr_result["date_of_birth"]["text"]
            self.fields["gender"].initial = ocr_result["sex_m_or_f"]["text"]
            self.fields["civil_status"].initial = ocr_result["civil_status"]["text"]
            self.fields["citizenship"].initial = ocr_result["citizenship"]["text"]
            self.fields["monthly_income"].initial = ocr_result["monthly_income"]["text"]
            self.fields["remarks"].initial = ocr_result["remarks"]["text"]
