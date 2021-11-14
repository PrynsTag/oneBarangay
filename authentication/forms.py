"""Create your authentication forms here."""
from django import forms
from django.core.validators import RegexValidator

from one_barangay.widgets import DatePickerWidget


class AccountSetupForm(forms.Form):
    """Forgot Password Form."""

    error_css_class = "is-invalid"
    required_css_class = "required"

    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: \
                    '+999999999'. Up to 15 digits allowed.",
    )
    contact_number = forms.CharField(
        validators=[phone_regex],
        help_text="Not required but highly recommended!",
        label="Phone Number",
        required=False,
        label_suffix="",
        max_length=17,
        widget=forms.TextInput(
            attrs={
                "placeholder": "+631234567891",
                "class": "",
                "type": "tel",
                "pattern": r"^\+?1?\d{9,15}$",
            }
        ),
    )
    address = forms.CharField(
        widget=forms.HiddenInput(
            attrs={
                "class": "",
                "placeholder": "Room/Floor/Unit #. Bldg Name, House Lot/Block, Street, Subdivision",
            }
        )
    )
    street = forms.CharField(widget=forms.HiddenInput(attrs={"class": ""}))
    zip_code = forms.CharField(widget=forms.HiddenInput(attrs={"class": ""}))
    country = forms.CharField(widget=forms.HiddenInput(attrs={"class": ""}))
    province = forms.CharField(widget=forms.HiddenInput(attrs={"class": ""}))
    city = forms.CharField(widget=forms.HiddenInput(attrs={"class": ""}))
    barangay = forms.CharField(widget=forms.HiddenInput(attrs={"class": ""}))
    region = forms.CharField(widget=forms.HiddenInput(attrs={"class": ""}))

    longitude = forms.CharField(widget=forms.HiddenInput(attrs={"class": ""}))
    latitude = forms.CharField(widget=forms.HiddenInput(attrs={"class": ""}))

    first_name = forms.CharField(
        label="First Name",
        label_suffix="",
        widget=forms.TextInput(attrs={"class": ""}),
    )
    middle_name = forms.CharField(
        label="Middle Name",
        label_suffix="",
        required=False,
        widget=forms.TextInput(attrs={"class": ""}),
    )
    last_name = forms.CharField(
        label="Last Name",
        label_suffix="",
        widget=forms.TextInput(attrs={"class": ""}),
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
        widget=DatePickerWidget(attrs={"class": "date-picker", "autocomplete": "off"}),
    )
    birth_place = forms.CharField(
        label="Birth Place",
        label_suffix="",
        widget=forms.TextInput(attrs={"class": ""}),
    )

    def __init__(self, *args, **kwargs):
        """Initialize AccountSetupForm form field value."""
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs["class"] += " form-control text-black"

        # for field in self.hidden_fields():
        #     field_name = field.html_name
        #     if field_name not in ["country", "latitude", "longitude"]:
        #         self.fields[field_name].widget.attrs["class"] += " hidden_el"


class ForgotPasswordForm(forms.Form):
    """Forgot Password Form."""

    error_css_class = "is-invalid"
    required_css_class = "required"

    email = forms.EmailField(
        label="Your Email",
        label_suffix="",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "juan_delacruz@gmail.com",
                "class": "form-control",
                "autofocus": True,
            }
        ),
    )


class LockAccountForm(forms.Form):
    """Lock Account Form."""

    error_css_class = "is-invalid"
    required_css_class = "required"

    password = forms.CharField(
        label="Your Password",
        label_suffix="",
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control",
                "pattern": r"^\S{8,}$",
                "onchange": "this.setCustomValidity(this.validity.patternMismatch ? "
                "'Must have at least 8 characters' : ''); "
                "if(this.checkValidity()) form.confirm_password.pattern = this.value;",
                "oninput": "password.setCustomValidity("
                "password.value !== confirm_password.value ? "
                "'Password is not the same with the confirm password.' : '')",
            }
        ),
    )

    def clean_password(self):
        """Clean password for minimum length."""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")

        if len(password) < 8:
            raise forms.ValidationError("The minimum password length is 8 characters.")

        return cleaned_data


class AuthenticationForm(LockAccountForm, ForgotPasswordForm):
    """Login, Signup and Forgot Password Form."""

    error_css_class = "is-invalid"
    required_css_class = "required"

    confirm_password = forms.CharField(
        label="Confirm Password",
        label_suffix="",
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Re-type Password",
                "class": "form-control",
                "pattern": r"^\S{8,}$",
                "onchange": "this.setCustomValidity(this.validity.patternMismatch ? "
                "'Please enter the same Password as above' : '');",
            }
        ),
    )
    remember_me = forms.BooleanField(
        label="Remember Me",
        label_suffix="",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    terms_condition = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    def clean(self):
        """Customize cleaning for form fields."""
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if (password and confirm_password) and (password != confirm_password):
            raise forms.ValidationError("Password and Confirm Password do not match.")

        return cleaned_data
