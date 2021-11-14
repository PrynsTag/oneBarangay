"""Create user_profile forms here."""
from dateutil import parser
from django import forms
from django.core.validators import RegexValidator

from one_barangay.widgets import DatePickerWidget


class UserProfileForm(forms.Form):
    """User Profile form."""

    error_css_class = "is-invalid"
    required_css_class = "required"

    first_name = forms.CharField(
        label="First Name",
        label_suffix="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "ex. (Juan)",
                "readonly": True,
                "class": "form-control text-black",
            }
        ),
    )

    last_name = forms.CharField(
        label="Last Name",
        label_suffix="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "ex. (Dela Cruz)",
                "readonly": True,
                "class": "form-control text-black",
            }
        ),
    )
    email = forms.EmailField(
        label="User Email",
        label_suffix="",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "name@company.com",
                "class": "form-control text-black",
                "readonly": True,
            }
        ),
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
            "%A, %b, %d %Y",
        ],
        widget=DatePickerWidget(attrs={"class": "form-control text-black date-picker", "autocomplete": "off", "readonly": True}),
    )

    # date_of_birth = forms.CharField(
    #     label="Birth Date",
    #     label_suffix="",
    #     widget=forms.TextInput(
    #         attrs={
    #             "placeholder": "ex. (January 20, 2020)",
    #             "readonly": True,
    #             "class": "form-control text-black",
    #         }
    #     ),
    # )

    gender = forms.ChoiceField(
        label="Gender",
        label_suffix="",
        required=False,
        disabled=True,
        choices=[
            ("M", "Male"),
            ("F", "Female"),
            ("O", "Others"),
        ],
        widget=forms.Select(
            attrs={
                "class": "form-select text-black mb-0",
                "aria-label": "Gender Select",
            },
        ),
    )

    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: \
            '+999999999'. Up to 15 digits allowed.",
    )
    phone_number = forms.CharField(
        validators=[phone_regex],
        label="Phone",
        label_suffix="",
        max_length=17,
        required=False,
        widget=forms.TextInput(
            attrs={
                "readonly": True,
                "placeholder": "+631234567891",
                "class": "form-control text-black",
                "type": "tel",
                "pattern": r"^\+?1?\d{9,15}$",
            }
        ),
    )

    address = forms.CharField(
        label="Address",
        label_suffix="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "1 I Marcelo Street, Valenzuela City, Metro Manila",
                "readonly": True,
                "class": "form-control text-black",
            }
        ),
    )

    def __init__(self, *args, request=None, **kwargs):
        """Initialize UserProfileForm attributes."""
        # TODO: Add age given date_of_birth.
        super().__init__(*args, **kwargs)
        if request.session.get("user"):
            first_name = request.session["user"].get("first_name")
            if first_name:
                self.fields["first_name"].initial = request.session["user"].get("first_name")
                self.fields["last_name"].initial = request.session["user"].get("last_name")
            elif request.session["user"]["display_name"]:
                display_name: list = request.session["user"]["display_name"].split()
                self.fields["first_name"].initial = display_name[0]
                self.fields["last_name"].initial = display_name[-1]
            else:
                self.fields["first_name"].initial = None
                self.fields["last_name"].initial = None
            self.fields["first_name"].initial = request.session["user"].get("first_name")
            self.fields["last_name"].initial = request.session["user"].get("last_name")
            self.fields["date_of_birth"].initial = (
                parser.parse(request.session["user"].get("date_of_birth")).strftime("%A, %b, %d %Y")
                if request.session["user"].get("date_of_birth")
                else None
            )
            self.fields["email"].initial = request.session["user"].get("email")
            self.fields["gender"].initial = request.session["user"].get("sex")
            self.fields["phone_number"].initial = request.session["user"].get("contact_number")
            self.fields["address"].initial = request.session["user"].get("address")
