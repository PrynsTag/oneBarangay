"""Create your complaint forms here."""
from datetime import datetime, timezone

from django import forms
from django.core.validators import RegexValidator, validate_email
from django.forms.utils import ErrorList


class ComplaintBaseForm(forms.Form):
    """Base form for complaint."""

    error_css_class = "is-invalid"
    required_css_class = "required"
    COMPLAINT_TYPE_CHOICES = (
        ("Public Disturbance", "Public Disturbance"),
        ("Gossip Problem", "Gossip Problem"),
        ("Lending Problem", "Lending Problem"),
        ("Obstruction", "Obstruction"),
        ("Others", "Others"),
    )
    COMPLAINT_STATUS_CHOICES = (
        ("For Review", "For Review"),
        ("Ongoing", "Ongoing"),
        ("Handed to Police", "Handed to Police"),
        ("Resolved", "Resolved"),
    )
    uid = forms.CharField(
        label="User I.D.",
        label_suffix="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control text-black",
            }
        ),
    )
    house_num = forms.CharField(
        label="House Number",
        label_suffix="",
        widget=forms.TextInput(attrs={"class": "form-control text-black"}),
    )
    complainant_name = forms.CharField(
        label="Complainant Name",
        label_suffix="",
        widget=forms.TextInput(attrs={"class": "form-control text-black"}),
    )
    email_regex = RegexValidator(
        regex=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
        message="Email address must be a valid and registered email "
        "from email address providers (e.g. Gmail, Outlook, etc.)",
    )
    email = forms.EmailField(
        validators=[email_regex, validate_email],
        help_text="Email address must be a valid and registered email "
        "from email address providers (e.g. Gmail, Outlook, etc.)",
        label="Email",
        label_suffix="",
        widget=forms.EmailInput(
            attrs={
                "pattern": r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                "placeholder": "Email",
                "class": "form-control text-black",
            }
        ),
    )
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: \
            '+999999999'. Up to 15 digits allowed.",
    )
    contact_number = forms.CharField(
        validators=[phone_regex],
        help_text="Phone number must be entered in the format: "
        "'+999999999'. Up to 15 digits allowed.",
        label="Phone Number",
        label_suffix="",
        max_length=17,
        widget=forms.TextInput(
            attrs={
                "placeholder": "+631234567891",
                "class": "form-control text-black",
                "type": "tel",
                "pattern": r"^\+?1?\d{9,15}$",
            }
        ),
    )
    date = forms.DateTimeField(
        label_suffix="",
        label="Date of Incident",
        input_formats=["%A, %B %d %Y, %H:%M %p"],
        widget=forms.DateTimeInput(
            attrs={"class": "form-control text-black", "autocomplete": "off"}
        ),
    )
    # TODO: Format address to chunks street, purok, etc.
    address = forms.CharField(
        label_suffix="",
        label="Address of Complainant",
        widget=forms.TextInput(
            attrs={
                "class": "form-control text-black",
                "aria-label": "Street Select",
            }
        ),
    )
    complaint_type = forms.ChoiceField(
        label="Type of Complaint",
        label_suffix="",
        widget=forms.Select(
            attrs={"class": "form-select text-black"},
        ),
        choices=COMPLAINT_TYPE_CHOICES,
    )
    complaint_status = forms.ChoiceField(
        label="Complaint Status",
        label_suffix="",
        widget=forms.Select(
            attrs={"class": "form-select text-black"},
        ),
        choices=COMPLAINT_STATUS_CHOICES,
    )
    comment = forms.CharField(
        label_suffix="",
        min_length=20,
        label="Reason of Complaint",
        widget=forms.Textarea(attrs={"class": "form-control text-black"}),
    )


class ComplaintDetailForm(ComplaintBaseForm):
    """Edit form for complaint."""

    complaint_id = forms.CharField(
        label="Complaint I.D.",
        label_suffix="",
        widget=forms.TextInput(attrs={"class": "form-control text-black"}),
    )

    image_url = forms.URLField(
        required=False, widget=forms.URLInput(attrs={"class": "form-control text-black"})
    )

    def __init__(self, *args, complaint=None, **kwargs):
        """Initialize ComplaintEditForm attributes."""
        super().__init__(*args, **kwargs)

        for field in self.fields:
            if complaint is not None:
                if field == "date":
                    self.fields[field].initial = (
                        complaint[field]
                        .replace(tzinfo=timezone.utc)
                        .astimezone(tz=None)
                        .strftime("%A, %B %d %Y, %I:%M %p")
                    )
                else:
                    self.fields[field].initial = complaint.get(field)

            self.fields[field].widget.attrs["readonly"] = True

    def clean(self):
        """Customize cleaning for form fields."""
        cleaned_data = super().clean()
        contact_number = self.fields["contact_number"].initial

        if contact_number.startswith("0"):
            contact_number = contact_number.replace("0", "+63", 1)
        if "-" in contact_number:
            contact_number = contact_number.replace("-", "")

        self.data = self.data.copy()
        self.data["contact_number"] = contact_number
        # if self.errors: TODO: Test and remove this later.
        if self.errors.get("contact_number"):
            self.errors["contact_number"] = ErrorList(
                [
                    "Data has been corrected."
                    "Click save again to confirm if these changes are OK."
                ]
            )
        return cleaned_data

    def clean_complaint_type(self):
        """Clean complaint_type form field manually."""
        complaint_type = self.cleaned_data.get("complaint_type")

        if complaint_type != self.fields["complaint_type"].initial:
            return self.fields["complaint_type"].initial
        else:
            return self.fields["complaint_type"].initial


class ComplaintCreateForm(ComplaintBaseForm):
    """Add form for complaint."""

    image = forms.ImageField(
        required=False,
        label_suffix="",
        label="Upload Proof of Incident",
        widget=forms.ClearableFileInput(attrs={"class": "form-control", "multiple": True}),
    )

    # TODO: Integrate this in OCR Module to get UID of user.
    def __init__(self, *args, request, **kwargs):
        """Initialize ComplaintEditForm attributes."""
        super().__init__(*args, **kwargs)

        user = request.session["user"]
        self.fields["uid"].initial = user.get("uid")
        self.fields["email"].initial = user.get("email")
        self.fields["house_num"].initial = user.get("house_num")
        self.fields["complainant_name"].initial = user.get("display_name")
        self.fields["contact_number"].initial = user.get("phone_number")
        self.fields["address"].initial = user.get("address")
        self.fields["complaint_status"].initial = "For Review"
        self.fields["date"].initial = datetime.now().strftime("%A, %B %d %Y, %I:%M %p")

    def clean(self):
        """Customize cleaning for form fields."""
        cleaned_data = super().clean()
        # Remove falsy values.
        cleaned_data = {key: value for key, value in cleaned_data.items() if value}

        return cleaned_data

    # TODO: Check if clean can do cleaning for readonly fields.
    def clean_uid(self):
        """Clean UID form field manually."""
        uid = self.cleaned_data.get("uid")

        if uid != self.fields["uid"].initial:
            return self.fields["uid"].initial
        else:
            return self.fields["uid"].initial

    def clean_house_num(self):
        """Clean house_num form field manually."""
        house_num = self.cleaned_data.get("house_num")

        if house_num != self.fields["house_num"].initial:
            return self.fields["house_num"].initial
        else:
            return self.fields["house_num"].initial

    def clean_complaint_status(self):
        """Clean clean_complaint_status form field manually."""
        complaint_status = self.cleaned_data.get("complaint_status")

        if complaint_status != self.fields["complaint_status"].initial:
            return self.fields["complaint_status"].initial
        else:
            return self.fields["complaint_status"].initial


class ComplaintContactForm(forms.Form):
    """Contact form for complaint."""

    error_css_class = "is-invalid"
    required_css_class = "required"

    email = forms.EmailField(
        help_text="Email address must be a valid and registered email "
        "from email address providers (e.g. Gmail, Outlook, etc.)",
        label="Email",
        label_suffix="",
        widget=forms.EmailInput(
            attrs={
                "pattern": r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                "placeholder": "Email",
                "class": "form-control text-black",
            }
        ),
    )
    date = forms.DateTimeField(
        label_suffix="",
        label="Appointment Date",
        input_formats=["%A, %B %d %Y, %H:%M %p"],
        widget=forms.DateTimeInput(
            attrs={"class": "form-control text-black", "autocomplete": "off"}
        ),
    )
    message = forms.CharField(
        label_suffix="",
        min_length=20,
        label="Message",
        widget=forms.Textarea(attrs={"class": "form-control text-black"}),
    )


class ComplaintDummyForm(forms.Form):
    """Dummy form for complaint dummy generation."""

    error_css_class = "is-invalid"
    required_css_class = "required"

    dummy_count = forms.IntegerField(
        label="How many Complaint to generate?",
        label_suffix="",
        widget=forms.NumberInput(attrs={"class": "form-control", "name": "dummy_form"}),
    )
